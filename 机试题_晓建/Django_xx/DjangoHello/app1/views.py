from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from app1.models import Article

from django.core.paginator import Paginator


# 纯字符串
def hello(request):
    return HttpResponse("lc  Hello, world. 首页.新的应用")


# 读取数据库,拼个字符串
def show_detail(request):
    first_article = Article.objects.all()[0]
    return HttpResponse(first_article.title)


# 读数据库+ 模板渲染(一个值)
def show_aticle(request):
    first_article = Article.objects.all()[0]
    return render(request, 'show.html', {'article': first_article})


# 读数据库+ 模板渲染(模板接收两个值)
def show_aticle2(request):
    first_article = Article.objects.all()[0]
    first_article1 = Article.objects.all()[1]
    return render(request, 'show2.html', {'article': first_article, 'article1': first_article1})


# 读数据库+ 模板渲染(模板接收多个值),for循环
# 总结一句话, Django的模板 和 flask自带的jin2使用方式是一样的
def show_aticles(request):
    articles = Article.objects.all()
    return render(request, 'blog/shows.html', {'articles': articles})


def index(request):
    page = request.GET.get('page')
    if page:
        page = int(page)
    else:
        page = 1
    print('page,', page)
    articles = Article.objects.all()
    top3_article_list = Article.objects.order_by('-publist_date')[:3]
    # Paginator 分页的
    p = Paginator(articles, 1)  # 每页几篇文章
    page_num = p.num_pages
    # print(p.num_pages)# 有几页

    # 获取第几页的文章
    page_article_list = p.page(page)
    if page_article_list.has_next():
        next_page = page + 1
    else:
        next_page = page
    if page_article_list.has_previous():
        previous_page = page - 1
    else:
        previous_page = page
    return render(request, 'blog/index.html',
                  {
                      # 'articles': articles,
                      'articles': page_article_list,
                      'page_num': range(1, page_num + 1),
                      'curr_page': page,
                      'next_page': next_page,
                      'previous_page': previous_page,
                      'top3_article_list': top3_article_list
                  })


def detail(request, article_id):
    articles = Article.objects.all()
    cur_article = None
    for article in articles:
        if article.article_id == article_id:
            cur_article = article
            break
    return render(request, 'blog/detail.html', {'article': cur_article})


def detail2(request, article_id):
    articles = Article.objects.all()
    cur_article = None
    previous_article_index = 0
    next_article_index = 0

    previous_article = None
    next_article = None
    # 得到当前文章的id
    # 如果用户随意输入了一个不存在的id ? 怎么办
    for article_index, article in enumerate(articles):
        previous_article_index = article_index - 1
        next_article_index = article_index + 1
        if article_index == 0:
            previous_article_index = 0
        elif article_index == len(articles) - 1:
            next_article_index = len(articles) - 1

        # if article_index==0:
        #     previous_article_index=0
        #     next_article_index=article_index+1
        # elif article_index==len(article)-1:
        #     previous_article_index=article_index-1
        #     next_article_index=len(article)-1
        # else:
        #     previous_article_index = article_index - 1
        #     next_article_index = article_index + 1

        # 确认当前文章是存在于数据库中的
        if article.article_id == article_id:
            cur_article = article
            # 根据上一页文章的id 获取到文章
            previous_article = articles[previous_article_index]
            next_article = articles[next_article_index]
            break
        # else:  # 不存在于数据库中
        #     if article_id > len(articles) - 1:
        #         cur_article = articles[len(articles) - 1]
        #         previous_article = articles[len(articles) - 2]
        #         next_article = articles[len(articles) - 1]
    return render(request, 'blog/detail2.html',
                  {
                      'article': cur_article,
                      'previous_article': previous_article,
                      'next_article': next_article,
                  })


def not_find_page(request, exception):
    # return HttpResponse('界面没有找到')
    return render(request, 'blog/page404.html')


from django.http import HttpResponseRedirect
def show_image(request):
    return render(request, 'showimage.html')
    # return HttpResponseRedirect()
