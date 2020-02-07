from datetime import datetime

from django.contrib import messages
from django.core.exceptions import ValidationError, PermissionDenied
from django.http import (
    Http404,
    HttpResponseBadRequest,
    HttpResponseRedirect,
)
from django.shortcuts import render, redirect, reverse, get_object_or_404

from .forms import CreateArticleForm
from .models import Article
from images.models import Image
from mtm.settings import TZ, NAME

def article(request, slug, article_id):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    try:
        article = Article.objects.get(id=article_id)
    except Article.DoesNotExist:
        messages.error(request, 'The specified article could not be found.')

        return redirect('users:index')

    if slug != article.slug:
        return HttpResponseRedirect(
            reverse('articles:article', args=[article.slug, article_id])
        )

    images = Image.objects.filter(album=article.album) if article.album else None
    return render(request, 'articles/article.html', {
        'article': article,
        'images': images,
        'images_preview': images[:14] if images and len(images) > 15 else images,
        'update_article_form': CreateArticleForm(instance=article),
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

    if form.is_valid():
        try:
            article = form.save()
        except ValidationError as error:
            messages.error(request, error)
        except PermissionDenied:
            messages.error(request, 'You do not have permission to create an article with that album.')

            return redirect('users:index')

        title = article.title
        punctuation = title[-1]
        messages.success(request, 'You have sucessfully created an article titled "%s%s"' % (title, '' if punctuation == '?' or punctuation == '!' or punctuation == '.' else '.'))

        return HttpResponseRedirect(
            reverse('articles:article', args=[article.slug, article.id])
        )

    messages.error(request, 'There was an error creating an article.')

    return redirect('users:index')

def update(request, slug, article_id):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    if not request.user.is_superuser:
        messages.error(request, 'You do not have permission to update this article.')

        return redirect('users:index')

    article = get_object_or_404(Article, id=article_id)
    form = CreateArticleForm(request.POST, instance=article)

    if form.is_valid():
        try:
            article = form.save()
        except ValidationError as error:
            messages.error(request, error)

        title = article.title
        punctuation = title[-1]
        messages.success(request, 'You have sucessfully updated "%s%s"' % (title, '' if punctuation == '?' or punctuation == '!' or punctuation == '.' else '.'))
    else:
        messages.error(request, 'The data entered was not valid.')

    return HttpResponseRedirect(
        reverse('articles:article', args=[article.slug, article.id])
    )

def delete(request, slug, article_id):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    if not request.user.is_superuser:
        messages.error(request, 'You do not have permission to update this article.')

        return redirect('users:index')

    try:
        article = get_object_or_404(Article, id=article_id)
    except Http404:
        messages.error(request, 'The specified article could not be found.')

        return redirect('users:index')

    try:
        Article.objects.delete(request, article)
    except ValidationError as errors:
        for error in errors:
            messages.error(request, error)

        return HttpResponseRedirect(
            reverse('articles:article', args=[article.slug, article.id])
        )

    title = article.title
    punctuation = title[-1]
    messages.success(request, 'You have successfully deleted the article "%s%s"' % (title, '' if punctuation == '?' or punctuation == '!' or punctuation == '.' else '.'))

    return redirect('users:index')
