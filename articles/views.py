from datetime import datetime

from django.contrib import messages
from django.core.exceptions import ValidationError, PermissionDenied
from django.http import (
    HttpResponseBadRequest,
    HttpResponseRedirect,
)
from django.shortcuts import render, redirect, reverse

from .forms import CreateArticleForm
from .models import Article
from images.models import Image
from mtm.settings import TZ, NAME

def article(request, article_title, article_id):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    try:
        article = Article.objects.get(id=article_id)
    except Article.DoesNotExist:
        messages.error(request, 'The specified article could not be found.')

        return redirect('users:index')

    if article_title != article.slug:
        return HttpResponseRedirect(
            reverse('articles:article', args=[article.slug, article_id])
        )

    return render(request, 'articles/article.html', {
        'article': article,
        'images': Image.objects.filter(album=article.album) if article.album else None,
        'CATEGORY_CHOICES': Article.CATEGORY_CHOICES,
        'user': request.user,
        'name': NAME,
        'year': datetime.now(TZ).year,
    })

def create(request):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    if not request.user.is_superuser:
        messages.error(request, 'You do not have permission to create an article.')

        return redirect('users:index')

    form = CreateArticleForm(request.POST)

    try:
        article = form.save()
    except ValidationError as error:
        messages.error(request, error)
    except PermissionDenied:
        messages.error(request, 'You do not have permission to create an article with that album.')

        return redirect('users:index')

    messages.success(request, 'You have sucessfully created an article titled "%s."' % article.title)

    return HttpResponseRedirect(
        reverse('articles:article', args=[article.slug, article.id])
    )
