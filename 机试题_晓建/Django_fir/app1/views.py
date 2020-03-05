from django.http import HttpResponse
from app1.models import Article
from django.shortcuts import render
from django.core.paginator import Paginator

# 纯字符串
def hello_world(request):
    return HttpResponse('我是app1中的hello_worlld,')


# 读取数据库,拼个字符串
def show_detail(request):
    first_article = Article.objects.all()[0]
    return HttpResponse(first_article.title)


# 读数据库+ 模板渲染(一个值)
def show_aticle(request):
    first_article = Article.objects.all()[0]
    return render(request, 'show.html', {'article': first_article})


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


def acticle_content(request):
    article = Article.objects.all()[0]
    title = article.title
    brief_content = article.brief_content
    content = article.content
    article_id = article.article_id
    publish_date = article.publish_date
    return_srt = f'title:{title},brief_content:{brief_content},content:{content},article_id:{article_id},publish_date:{publish_date}'

    return HttpResponse(return_srt)
    # return HttpResponse(articls.title)


def get_index_page(request):
    all_article = Article.objects.all()
    return render(request, 'app1/index.html', {'article_list': all_article})


def not_find_page(request, exception):
    # return HttpResponse('界面没有找到')
    return render(request, 'blog/page404.html')




def get_detail_page(request, article_id):
    all_article = Article.objects.all()
    curr_article = None
    previous_index = 0
    next_index = 0
    previous_article = None
    next_article = None
    # 迭代器,能够获取角标index
    for index, article in enumerate(all_article):
        if index == 0:
            previous_index = 0
            next_index = index + 1
        elif index == len(all_article) - 1:
            previous_index = index - 1
            next_index = index
        else:
            previous_index = index - 1
            next_index = index + 1
        if article.article_id == article_id:
            curr_article = article
            previous_article = all_article[previous_index]
            next_article = all_article[next_index]
            # break
            return render(request, 'app1/detail.html',
                  {
                      'curr_article': curr_article,
                      'previous_article': previous_article,
                      'next_article': next_article
                  })
