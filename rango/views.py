import uuid

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rango.models import Category, UserProfile
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
        per_pagecount=5
        page_limit=5
        page_obj=PageClass(current_page,len(pages),category_name_slug,per_pagecount,page_limit)
        context_dict['category'] = category
        context_dict['pages'] = pages[page_obj.start():page_obj.end()]
        context_dict['page_str']=page_obj.page_str()
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
        category=Category.objects.create(name=category_name)
        category.save()
        print("保存category")
        return redirect(reverse('rango:index'))
    print("返回添加页面")
    return render(request, 'rango/add_category.html')

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    if category is None:
        return redirect(reverse('rango:show_category'))

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
        page=Page.objects.create(title=title, url=url, category=category)
        page.save()
        return redirect(reverse('rango:show_category', kwargs={'category_name_slug':category_name_slug}))

    context_dict = {'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)


def register(request):
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
            status = False
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse('rango:index'))
                    # return HttpResponse(json.dumps({'flag': True}))
                else:
                    return HttpResponse("Your Rango account is disabled")
            else:
                print(f'Invalid login details: {username}, {password}')

                return JsonResponse({'flag': False})

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

def test(request):
    return render(request, 'rango/test.html')

def show_profile(request):

    user=getattr(request,"user",None)
    username=user.username
    userProfile=UserProfile.objects.get(user=user)
    time=userProfile.date
    webiste=userProfile.website
    context_dic={'username':username,'time':time,'webiste':webiste}

    return render(request, 'rango/profile.html',context=context_dic)

class PageClass:
    def __init__(self,current_page,data_count,categoryname,page_count=5,page_limit=5):
        self.current_page=current_page
        self.data_count=data_count
        self.page_count=page_count
        self.page_limit=page_limit
        self.categoryname=categoryname
    def start(self):
        return (self.current_page-1)*self.page_count
    def end(self):
        return self.current_page*self.page_count
    @property
    def total_pages(self):
        v,mod=divmod(self.data_count,self.page_count)
        if mod:
            v+1;
        return v
    def page_str(self):
        page_list=[]
        if self.total_pages<self.page_limit:
            start_index=1
            end_index=self.total_pages+1
        else:
           if self.current_page<=(self.page_limit+1)/2:
               start_index=1
               end_index=self.page_limit+1
           else:
               start_index=self.current_page-(self.page_limit-1)/2
               end_index=self.current_page+(self.page_limit+1)/2
               if(self.current_page+(self.page_limit-1)/2)>self.total_pages:
                   end_index=self.total_pages+1
                   start_index=self.total_pages-self.page_limit+1
        if self.current_page == 1:
            prev = '<a class ="page " href="#">previous page</a>'
        else:
            prev = '<a class ="page" href="/rango/category/%s/?p=%s">previous page</a>' % (
                self.categoryname, self.current_page - 1,)
        page_list.append(prev)
        if(start_index==end_index):
            temp = '<a class="page active" href="/rango/category/%s/?p=%s">%s</a>' % (self.categoryname, start_index,start_index)
            next = '<a class ="page " href="#">next page</a>'
            page_list.append(temp)
        else:
            for i in range(int(start_index), int(end_index)):
                if i == self.current_page:
                    temp = '<a class="page active" href="/rango/category/%s/?p=%s">%s</a>' % (self.categoryname, i, i)
                else:
                    temp = '<a class="page" href="/rango/category/%s/?p=%s">%s</a>' % (self.categoryname, i, i)
                page_list.append(temp)
            if self.current_page == self.total_pages:
                next = '<a class ="page " href="#">next page</a>'
            else:
                next = '<a class ="page " href="/rango/category/%s/?p=%s">next page</a>' % (
                    self.categoryname, self.current_page + 1,)
        page_list.append(next)
        jump = """<input type='text'/><a onclick='jumpTo(this,"/rango/category/%s/?p=");'>Go</a>
                     <script>
                        function jumpTo(ths,base){
                           var val=ths.previousSibling.value;
                           location.href=base+val;}
                     </script>"""%(self.categoryname,)
        page_list.append(jump)
        page_str="".join(page_list)
        page_str=mark_safe(page_str)
        return page_str


def search(request):
    if request.method == "GET":
        render(request, 'rango/category.html')

    context_dict = {}
    category_name_slug = request.POST['category']
    print(category_name_slug)
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
        print(context_dict)
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None

    return render(request, 'rango/category.html', context=context_dict)


def pre_check_username(request):
    username = request.POST.get('username')
    user_list = UserProfile.objects.filter(sname=username)
    if user_list:
        return JsonResponse({'flag': True})
    else:
        return JsonResponse({'flag': False})



