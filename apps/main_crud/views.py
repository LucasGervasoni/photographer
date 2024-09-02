from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from apps.main_crud.models import Order, OrderEditorAssignment
from django.contrib.auth.models import Group
from apps.main_crud.forms import OrderForm  
from apps.pictures.models import OrderImageGroup
from django.db.models import OuterRef, Subquery 
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin
from django.utils.dateparse import parse_date
from django.db.models import Q

from apps.users.models import CustomUser

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
            full_name = f"{user.first_name} {user.last_name}"

            # Filter to get orders the user is involved in or is assigned as an editor
            queryset = Order.objects.all()

            if not user.is_superuser:
                queryset = queryset.filter(
                    Q(appointment_team_members__icontains=user.username) |
                    Q(appointment_team_members__icontains=full_name) |
                    Q(ordereditorassignment__assigned_editor=user)
                )

            # Apply filters for status, search query, and date range
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
            if start_date and end_date:
                queryset = queryset.filter(order_created_at__date__range=[parse_date(start_date), parse_date(end_date)])

            # Annotate each Order with the latest 3D scan URL from OrderImageGroup
            latest_scan_url = OrderImageGroup.objects.filter(
                order=OuterRef('pk'),
                scan_url__isnull=False,
            ).exclude(scan_url='').order_by('-created_at').values('scan_url')[:1]

            queryset = queryset.annotate(latest_scan_url=Subquery(latest_scan_url))

            # Prefetch related OrderEditorAssignment for editor assignment handling
            queryset = queryset.prefetch_related('ordereditorassignment')

            return queryset.order_by('-order_created_at')

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            try:
                # Attempt to fetch all users in the Editor group
                editor_group = Group.objects.get(name='Editor')
                context['editors'] = editor_group.user_set.all()
            except Group.DoesNotExist:
                # If the Editor group does not exist, set an empty queryset or handle it as needed
                context['editors'] = Group.objects.none()
            return context

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
        full_name = f"{user.first_name} {user.last_name}"

        # Filter to get orders the user is involved in or is assigned as an editor
        queryset = Order.objects.all()

        if not user.is_superuser:
            queryset = queryset.filter(
                Q(appointment_team_members__icontains=user.username) |
                Q(appointment_team_members__icontains=full_name) |
                Q(ordereditorassignment__assigned_editor=user)
            )

        # Apply filters for status, search query, and date range
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
        if start_date and end_date:
            queryset = queryset.filter(order_created_at__date__range=[parse_date(start_date), parse_date(end_date)])

        # Annotate each Order with the latest 3D scan URL from OrderImageGroup
        latest_scan_url = OrderImageGroup.objects.filter(
            order=OuterRef('pk'),
            scan_url__isnull=False,
        ).exclude(scan_url='').order_by('-created_at').values('scan_url')[:1]

        queryset = queryset.annotate(latest_scan_url=Subquery(latest_scan_url))

        # Prefetch related OrderEditorAssignment for editor assignment handling
        queryset = queryset.prefetch_related('ordereditorassignment')

        return queryset.order_by('-order_created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            # Attempt to fetch all users in the Editor group
            editor_group = Group.objects.get(name='Editor')
            context['editors'] = editor_group.user_set.all()
        except Group.DoesNotExist:
            # If the Editor group does not exist, set an empty queryset or handle it as needed
            context['editors'] = Group.objects.none()
        return context

# Update orders by select button in html
class UpdateOrderStatusView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Order
    fields = ['order_status']

    def form_valid(self, form):
        form.save()
        return redirect('userOrders--page')
    
class AssignOrderEditorView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    
    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        
        if request.user.is_superuser and order.order_status == 'Production':
            assigned_editor_id = request.POST.get('assigned_editor')
            order_editor_assignment, created = OrderEditorAssignment.objects.get_or_create(order=order)
            if assigned_editor_id:
                order_editor_assignment.assigned_editor_id = assigned_editor_id
            else:
                order_editor_assignment.assigned_editor = None  # Clear the assigned editor
            order_editor_assignment.save()

            # Set session variable to keep listInfo open
            request.session['open_list_info'] = order_id
        
        # Clear the session variable after it's been used
        if 'open_list_info' in request.session:
            del request.session['open_list_info']

        return redirect('userOrders--page')