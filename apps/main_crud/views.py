from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from apps.main_crud.models import Order
from apps.main_crud.forms import OrderForm
from apps.pictures.models import OrderImageGroup
from django.db.models import OuterRef, Subquery, Q, Count, Case, When, Value, CharField
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin
from django.utils.dateparse import parse_date

#Create
class OrderCreateView(GroupRequiredMixin,LoginRequiredMixin,CreateView):
    group_required = ['Admin']
    login_url = reverse_lazy('login')
    model = Order
    form_class = OrderForm
    template_name = 'main_crud/admin/order_form.html'
    success_url = reverse_lazy('adminOrders--page')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Order'
        context['button'] = 'Create'
        context['class'] = 'd-block'
        return context


#List Order for Admin
class AdminListOrders(GroupRequiredMixin,LoginRequiredMixin,ListView):
        group_required = ['Admin']
        login_url = reverse_lazy('login')
        model = Order
        template_name = "main_crud/admin/adminListOrder.html"
        paginate_by = 50
        
        #Return the orders by user
        def get_queryset(self):
                user = self.request.user
                queryset = Order.objects.all()
                
                 # Construct the full name of the user
                full_name = f"{user.first_name} {user.last_name}"
                
                # Subquery to get the count of scan URLs for each order
                scan_url_count_subquery = OrderImageGroup.objects.filter(
                    order=OuterRef('pk'),
                    services__icontains="3d scan",
                    scan_url__isnull=False
                ).values('order').annotate(count=Count('scan_url')).values('count')[:1]

                # Subquery to get the first scan URL
                first_scan_url_subquery = OrderImageGroup.objects.filter(
                    order=OuterRef('pk'),
                    services__icontains="3d scan",
                    scan_url__isnull=False
                ).order_by('created_at').values('scan_url')[:1]

                # Subquery to get the most recent scan URL
                recent_scan_url_subquery = OrderImageGroup.objects.filter(
                    order=OuterRef('pk'),
                    services__icontains="3d scan",
                    scan_url__isnull=False
                ).order_by('-created_at').values('scan_url')[:1]

                queryset = Order.objects.annotate(
                    scan_url_count=Subquery(scan_url_count_subquery),
                    latest_scan_url=Case(
                        When(scan_url_count__gt=1, then=Subquery(recent_scan_url_subquery)),
                        default=Subquery(first_scan_url_subquery),
                        output_field=CharField(),
                    )
                )
                

                # Check if the user is not an editor or superuser
                if not user.is_superuser and not user.groups.filter(name='Admin').exists():
                        # Filter orders by checking if the username or full name is in the appointment_team_members field
                        queryset = queryset.filter(
                                Q(appointment_team_members__icontains=user.username) |
                                Q(appointment_team_members__icontains=full_name)
                        )

                # Filter by status
                status = self.request.GET.get('status')
                if status:
                 queryset = queryset.filter(order_status=status)
                 
                 # Filter by search query
                search_query = self.request.GET.get('search')
                if search_query:
                 queryset = queryset.filter(
                        Q(appointment_team_members__icontains=search_query) |
                        Q(customer__icontains=search_query) |
                        Q(appointment_date__icontains=search_query) |
                        Q(address__icontains=search_query) |
                        Q(appointment_items__icontains=search_query) |
                        Q(order_status__icontains=search_query) |
                        Q(order_created_at__icontains=search_query)
                )
                
                 # Filtro por data de criação (intervalo)
                start_date = self.request.GET.get('start_date')
                end_date = self.request.GET.get('end_date')
                start_date_parsed = parse_date(start_date) if start_date else None
                end_date_parsed = parse_date(end_date) if end_date else None

                if start_date_parsed and end_date_parsed:
                 queryset = queryset.filter(order_created_at__date__range=[start_date_parsed, end_date_parsed])

                # Ordena pelo campo order_created_at
                return queryset.order_by('-order_created_at')

#Update Order

class OrderUpdateView(GroupRequiredMixin,LoginRequiredMixin,UpdateView):
    group_required = ['Admin']
    login_url = reverse_lazy('login')
    model = Order
    form_class = OrderForm
    template_name = 'main_crud/admin/order_form.html'
    success_url = reverse_lazy('adminOrders--page')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Order'
        context['button'] = 'Update'
        context['class'] = 'd-none'
        return context
    
#Delete

class OrderDeleteView(GroupRequiredMixin,LoginRequiredMixin,DeleteView):
    group_required = ['Admin']
    login_url = reverse_lazy('login')
    model = Order
    template_name = 'main_crud/admin/deleteOrder.html'
    success_url = reverse_lazy('adminOrders--page')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Order'
        context['button'] = 'Confirm Delete'
        return context

#List Orders for user
class UserPageOrders(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Order
    template_name = "main_crud/user/UserOrdersList.html"
    paginate_by = 50

    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.all()

        # Construct the full name of the user
        full_name = f"{user.first_name} {user.last_name}"

        # Subquery to get the count of scan URLs for each order
        scan_url_count_subquery = OrderImageGroup.objects.filter(
            order=OuterRef('pk'),
            services__icontains="3d scan",
            scan_url__isnull=False
        ).values('order').annotate(count=Count('scan_url')).values('count')[:1]

        # Subquery to get the first scan URL
        first_scan_url_subquery = OrderImageGroup.objects.filter(
            order=OuterRef('pk'),
            services__icontains="3d scan",
            scan_url__isnull=False
        ).order_by('created_at').values('scan_url')[:1]

        # Subquery to get the most recent scan URL
        recent_scan_url_subquery = OrderImageGroup.objects.filter(
            order=OuterRef('pk'),
            services__icontains="3d scan",
            scan_url__isnull=False
        ).order_by('-created_at').values('scan_url')[:1]

        queryset = Order.objects.annotate(
            scan_url_count=Subquery(scan_url_count_subquery),
            latest_scan_url=Case(
                When(scan_url_count__gt=1, then=Subquery(recent_scan_url_subquery)),
                default=Subquery(first_scan_url_subquery),
                output_field=CharField(),
            )
        )


        # Filter by user, status, search, and date
        if not user.is_superuser and not user.groups.filter(name='Editor').exists():
            queryset = queryset.filter(
                Q(appointment_team_members__icontains=user.username) |
                Q(appointment_team_members__icontains=full_name)
            )

        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(order_status=status)

        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(appointment_team_members__icontains=search_query) |
                Q(customer__icontains=search_query) |
                Q(appointment_date__icontains=search_query) |
                Q(address__icontains=search_query) |
                Q(appointment_items__icontains=search_query) |
                Q(order_status__icontains=search_query) |
                Q(order_created_at__icontains=search_query)
            )

        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        start_date_parsed = parse_date(start_date) if start_date else None
        end_date_parsed = parse_date(end_date) if end_date else None

        if start_date_parsed and end_date_parsed:
            queryset = queryset.filter(order_created_at__date__range=[start_date_parsed, end_date_parsed])

        return queryset.order_by('-order_created_at')


# Update orders by select button in html
class UpdateOrderStatusView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Order
    fields = ['order_status']

    def form_valid(self, form):
        form.save()
        return redirect('userOrders--page')