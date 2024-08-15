from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from .models import Order
from django.urls import reverse_lazy


from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models import Q

#List Orders for user
class UserPageOrders(LoginRequiredMixin,ListView):
        login_url = reverse_lazy('login')
        model = Order
        template_name = "main_crud/user/UserOrdersList.html"
        paginate_by = 10
        
        #Return the orders by user
        def get_queryset(self):
                user = self.request.user
                queryset = Order.objects.all()
                
                 # Construct the full name of the user
                full_name = f"{user.first_name} {user.last_name}"
                

                # Check if the user is not an editor or superuser
                if not user.is_superuser and not user.groups.filter(name='Editor').exists():
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
                
                return queryset.order_by('-id')

# Update orders by select button in html
class UpdateOrderStatusView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Order
    fields = ['order_status']

    def form_valid(self, form):
        form.save()
        return redirect('userOrders--page')