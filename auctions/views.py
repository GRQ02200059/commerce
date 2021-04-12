from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .models import Bids
from .models import Comments
from .models import User
from django.shortcuts import render,redirect,reverse
from .models import  Watchlists
from  .models import Auction_lists
def data_fresh(request):
    user=request.user.username
    nums=Watchlists.objects.filter(user=user,mark="add")
    num=len(nums)
    print(num)
    context={"data":num}
    return JsonResponse(context)

def after_bids(request):
    name=request.POST.get("name")
    bid=request.POST.get("bid")
    user=request.POST.get("user")
    # print(name,bid,user)
    the_bids=Bids(name=name,bid=bid,user=user)
    the_bids.save()
    url = reverse('detail', kwargs={'name': name})
    return redirect(url)
def the_category(request,category):
    list=Auction_lists.objects.filter(category=category)
    return render(request, "auctions/index.html", {"lists": list,"title":"categories"})


def detail(request,name):
    print(name)
    # cur_user=request.POST.get("user")
    cur_user=request.user

    auction1=Auction_lists.objects.get(name=name)
    # print(auction1.image_url)
    state=auction1.state
    owner=auction1.last_man


    the_bids=Bids.objects.filter(name=name)
    all_bids=[]
    if the_bids.exists():
        # print("="*30)
        # print(the_bids)
        for b in the_bids:
            # print("+"*30)
            # print(b.bid)
            # print("+" * 30)
            all_bids.append(b.bid)
        largest=max(all_bids)

    else:
        largest=auction1.price
    # print("largest="+str(largest))
    nums=len(all_bids)




    user=request.user.username
    print("3"*30)
    print(user)
    print("3" * 30)
    try:
        mark=Watchlists.objects.get(name=name,user=user)
    except Exception:
        m = "white"
    else:
        m=mark.mark
        if(m=="add"):
            m="blue"
        else:
            m = "white"


    comments=Comments.objects.filter(name=name)

    the_comments=[]
    if comments !=None:
        for c in comments:
            the_comments.append(c.comment)
    print("="*30)
    print(m)
    print("=" * 30)



    return render(request, "auctions/detail.html", {"state":state,"owner":owner, "currentuser":cur_user.username,"list":auction1, "comments":the_comments, "bids":largest, "nums":nums, "col":m})
    # else:
    #     url = reverse('detail', kwargs={'name': name})
    #     return redirect(url)

def close(request):
    entry=request.POST.get("entry")
    state=request.POST.get("state")
    print(entry,state)
    owners=Bids.objects.filter(name=entry)
    if(len(owners)==0):
        last_man="null"
    else:
        max=owners[0].bid
        last_man=owners[0]
        for owner in owners:
            if owner.bid>max:
                last_man=owner.user


    Auction_lists.objects.filter(name=entry).update(state="close",last_man=last_man)

    url = reverse('detail', kwargs={'name': entry})
    return redirect(url)






def after_comments(request):
    comment=request.POST.get("comment")
    name=request.POST.get("name")
    # print(comment,name)
    the_comment=Comments(name=name,comment=comment)
    the_comment.save()
    url = reverse('detail', kwargs={'name': name})
    return redirect(url)
def wl(request):
    print()
    print("+"*30)
    print(request.POST)
    print("+"*30)
    user=request.POST.get("user")
    name=request.POST.get("name")
    action=request.POST.get("action")
    try:

        the_watchlist=Watchlists.objects.get(user=user,name=name)
    except Exception:
        print("不存在")
        the_watchlist = Watchlists(user=user, name=name, mark=action)
        the_watchlist.save()
        print("已" + action + "收藏")
        url = reverse('detail', kwargs={'name': name})
        return redirect(url)
    else:
        print("存在")
        Watchlists.objects.filter(user=user,name=name).update(mark=action)

        print("已" + action + "收藏")
        url = reverse('detail', kwargs={'name': name})
        return redirect(url)

def index(request):
    lists=Auction_lists.objects.all()
    # print(type(lists))
    # for list in lists:
    #     print("+"*30)
    #     print(list.name)
    #     print("+" * 30)

    return render(request, "auctions/index.html",{"lists":lists,"title":"Active Listing"})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

def categories(request):

    return  render(request,"auctions/category.html")
def create_list(request):
    return render(request,"auctions/create_list.html")
def after_create(request):
    user=request.POST.get("user")

    title=request.POST.get("title")
    desc=request.POST.get("descr")
    bid=request.POST.get("s_bid")
    image_url=request.POST.get("image_url")
    category=request.POST.get("xueli")
    # print(title,desc,bid,image_url,category)
    auction1=Auction_lists(name=title,desc=desc,price=bid,image_url=image_url,category=category,user=user)
    auction1.save()
    # print("已保存")

    return HttpResponseRedirect(reverse("index"))
def watchlist(request,user):
    print(user)
    all_list=[]
    the_lists=Watchlists.objects.filter(user=user,mark="add")
    for list in the_lists:
        auc=Auction_lists.objects.get(name=list.name)
        all_list.append(auc)
    return render(request,"auctions/index.html",{"lists":all_list,"title":"Watchlists"})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            print("=" * 30)
            print("333")
            user = User.objects.create_user(username, email, password)
            print("="*30)
            print("333")
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
