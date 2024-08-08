from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from .models import Order
from django.urls import reverse_lazy


from django.contrib.auth.mixins import LoginRequiredMixin

#List Orders for user
class UserPageOrders(LoginRequiredMixin,ListView):
        login_url = reverse_lazy('login')
        model = Order
        template_name = "main_crud/user/UserOrdersList.html"
        paginate_by = 3
        
        #Return the orders by user
        def get_queryset(self):
                user = self.request.user
                queryset = Order.objects.all()

                # Check if the user is not an editor or superuser
                if not user.is_superuser and not user.groups.filter(name='Editor').exists():
                        queryset = queryset.filter(user=user)

                # Filter by status
                status = self.request.GET.get('status')
                if status:
                 queryset = queryset.filter(order_status=status)
                
                return queryset.order_by('-date')

# Update orders by select button in html
class UpdateOrderStatusView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Order
    fields = ['order_status']

    def form_valid(self, form):
        form.save()
        return redirect('userOrders--page')