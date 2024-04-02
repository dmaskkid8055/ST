from django.shortcuts import render
from shop.models import Product
from cart.models import Cart,Order,Account
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
@login_required
def cart_view(request):
    #For displaying cart for the current user
    u=request.user
    total=0
    c=Cart.objects.filter(user=u)
    #to find the total amount
    for i in c:
        total=total+i.quantity*i.product.price
    return render(request,'cart.html',{'c':c,'total':total})

@login_required

def addtocart(request,p): #For adding a particular product to Cart table
    p=Product.objects.get(id=p)
    u=request.user
    try:
        cart=Cart.objects.get(user=u,product=p)
        if(p.stock>0):
            cart.quantity+=1
            cart.save()
            p.stock -= 1
            p.save()
    except:
        if(p.stock>0):

            cart=Cart.objects.create(product=p,user=u,quantity=1)
            cart.save()
            p.stock -= 1
            p.save()

    return cart_view(request)


def cart_remove(request,p):
    p = Product.objects.get(id=p)
    u = request.user
    try:
        cart = Cart.objects.get(user=u, product=p)

        if(cart.quantity>1):
            cart.quantity -= 1
            cart.save()
            p.stock += 1
            p.save()

        else:
            cart.delete()
            p.stock += 1
            p.save()
    except:
        pass
    return cart_view(request)


def full_remove(request,p):
    p = Product.objects.get(id=p)
    u = request.user
    try:
        cart = Cart.objects.get(user=u, product=p)
        cart.delete()
        p.stock += cart.quantity
        p.save()
    except:
        pass


    return cart_view(request)
@login_required
def orderform(request):
    if(request.method=="POST"):
        print('hello')
        a=request.POST['a']
        p=request.POST['p']
        n=request.POST['n']

        u=request.user

        c=Cart.objects.filter(user=u)

        total=0
        for i in c:
            total=total+i.quantity*i.product.price
        print(total)

        try:
            ac=Account.objects.get(acctnum=n)
            if(ac.amount >= total):
                ac.amount=ac.amount-total

                ac.save()
                for i in c:
                    o=Order.objects.create(user=u,product=i.product,address=a,phone=p,no_of_items=i.quantity,order_status="paid")
                    o.save()

                c.delete()
                msg= "Order Placed Successfully"
                print(msg)
                return render(request,'orderdetail.html',{'message':msg})
            else:
                print(msg)
                msg = "Insufficient Account. You can't Place Order"
                return render(request, 'orderdetail.html',{'message': msg})



        except:
            pass

    return render(request,'orderform.html')

@login_required
def orderview(request):
    u=request.user
    o=Order.objects.filter(user=u)

    return render(request,'orderview.html',{'o':o,'u':u.username})