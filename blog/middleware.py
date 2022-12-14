from .models import IPAddress


def SaveIPAddressmiddleware(get_response):
    

    def middleware(request):
        
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        response = get_response(request)


        try:
            ip_address = IPAddress.objects.get(ip_address=ip)
        except:
            ip_address = IPAddress.objects.create(ip_address=ip)

        try:
            if request.user.is_authenticated:
                customer = request.user.customer
                customer.ip_address = ip_address
                customer.save()
        except:
            pass
        return response

    return middleware
