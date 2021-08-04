import uuid

from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm
from django.shortcuts import redirect
from django.urls import reverse
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime
from django.utils.safestring import mark_safe

def index(request):
    # - means descending order, remove - is ascending order
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[0:5]

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list

    visitor_cookie_handler(request)
    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    context_dict = {}
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    return render(request, 'rango/about.html', context=context_dict)


def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        current_page = request.GET.get('p', 1)
        current_page = int(current_page)
        start = (current_page - 1) * 5
        end = current_page * 5
        context_dict['category'] = category
        context_dict['pages'] = pages[start:end]
        page_count,page_mode= divmod(len(pages),5)
        page_list=[]
        if page_mode:
            page_count+=1
        for i in range(1, page_count+1):
            if i == current_page:
                temp = '<a class="page active" href="/rango/category/%s/?p=%s">%s</a>' % (category_name_slug, i, i)
            else:
                temp = '<a class="page" href="/rango/category/%s/?p=%s">%s</a>' % (category_name_slug, i, i)
            page_list.append(temp)
        page_str="".join(page_list)
        page_str=mark_safe(page_str)
        context_dict['page_str']=page_str
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None
        context_dict['data'] = None

    return render(request, 'rango/category.html', context=context_dict)

@login_required
def add_category(request):

    """
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('/rango/')
        else:
            print(form.errors)
    return render(request, 'rango/add_category.html', {'form': form})
    """
    print("进入函数")
    if request.method == 'POST':
        category_name = request.POST['category_name']
        Category.objects.create(name=category_name, slug=uuid.uuid1)
        Category.save()
        print("保存category")
        return redirect('rango/')
    print("返回添加页面")
    return render(request, 'rango/add_category.html')


@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    if category is None:
        return redirect('/rango/')

    """
    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)
        print(request.POST['title'])
        print(request.POST['url'])
        print("slug", category_name_slug)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
            else:
                print(form.errors)
    
    """
    if request.method == 'POST':
        title = request.POST['title']
        print(title)
        url = request.POST['url']
        Page.objects.create(title=title, url=url, category=category)
        return redirect(reverse('rango:show_category', kwargs={'category_name_slug':category_name_slug}))

    context_dict = {'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)


def register(request):
    """
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'rango/register.html', context={'user_form': user_form,
                                                           'profile_form': profile_form,
                                                           'registered': registered})
    """

    registered = False
    if request.method == 'POST':
        print(request.POST['username'])
        print(request.POST['email'])
        print(request.POST['password'])
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    return render(request, 'rango/register.html', locals())


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print('username:', username)
        print('password:', password)
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse("Your Rango account is disabled")
        else:
            print(f'Invalid login details: {username}, {password}')
            return HttpResponse("Invalid login details supplied")
    else:
        return render(request, 'rango/login.html')


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')


def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))


def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie
    request.session['visits'] = visits


def show_profile(request):
    return render(request, 'rango/profile.html')