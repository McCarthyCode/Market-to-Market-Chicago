import os

from datetime import datetime

from django.contrib import messages
from django.core.exceptions import ValidationError, PermissionDenied
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.http import (
    Http404,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseRedirect,
)
from django.shortcuts import render, redirect, reverse, get_object_or_404

from .forms import AuthorForm, ArticleForm
from .models import AuthorImage, Author, Article
from images.models import Image
from mtm.settings import TZ, NAME, ARTICLES_PER_PAGE, MEDIA_ROOT

def article(request, slug, article_id):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    article = get_object_or_404(Article, id=article_id)

    if slug != article.slug:
        return HttpResponseRedirect(
            reverse('articles:article', args=[article.slug, article_id])
        )

    images = Image.objects.filter(album=article.album) if article.album else None
    return render(request, 'articles/article.html', {
        'article': article,
        'images': images,
        'images_preview': images[:14] if images and len(images) > 15 else images,
        'update_article_form': ArticleForm(instance=article),
        'user': request.user,
        'name': NAME,
        'year': datetime.now(TZ).year,
    })

def by_page(request):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    category = request.GET.get('category', '')
    page = request.GET.get('page', '')

    if not page:
        page = 1
    else:
        page = int(page)

    if not category:
        articles = Article.objects.all().order_by('-date_updated')
    else:
        slug_to_id = {
            'nightlife': 0,
            'restaurants': 1,
            'arts-and-entertainment': 2,
            'health-and-fitness': 3,
            'sports': 4,
            'non-profit': 5,
        }

        articles = Article.objects.filter(category=slug_to_id[category]).order_by('-date_updated')

    articles_paginator = Paginator(articles, ARTICLES_PER_PAGE)

    try:
        return render(request, 'articles/article_category.html', {
            'articles': articles_paginator.page(page).object_list,
        })
    except EmptyPage as exception:
        return HttpResponse(exception, status=204)

def create(request):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    if not request.user.is_superuser:
        return HttpResponseForbidden()

    form = ArticleForm(request.POST)

    if form.is_valid():
        try:
            article = form.save()
        except ValidationError as error:
            messages.error(request, error)

            return redirect('users:index')
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
        return HttpResponseForbidden()

    article = get_object_or_404(Article, id=article_id)
    form = ArticleForm(request.POST, instance=article)

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
        return HttpResponseForbidden()

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

def author(request, slug, author_id):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    author = get_object_or_404(Author, id=author_id)

    if slug != author.slug:
        return HttpResponseRedirect(
            reverse('articles:author', args=[author.slug, author_id])
        )

    return render(request, 'articles/author.html', {
        'author': author,
        'update_author_form': AuthorForm(instance=author),
        'name': NAME,
        'year': datetime.now(TZ).year,
    })

def create_author(request):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    if not request.user.is_superuser:
        return HttpResponseForbidden()

    form = AuthorForm(request.POST, request.FILES)

    if form.is_valid():
        author = form.save()

        if 'image' in request.FILES:
            profile_image = AuthorImage.objects.create(image=request.FILES.get('image'))
            profile_image.image_ops()
            profile_image.save()
            author.profile_image = profile_image

        author.save()

        full_name = author.full_name
        punctuation = full_name[-1]
        messages.success(request, 'You have successfully created an author named "%s%s"' % (full_name, '' if punctuation == '?' or punctuation == '!' or punctuation == '.' else '.'))

        return redirect('users:index')

    messages.error(request, 'There was an error creating an author.')

    if request.user.is_superuser:
        return render(request, 'users/index.html', {
            'create_person_form': PersonForm(),
            'create_author_form': AuthorForm(request.POST),
            'create_article_form': ArticleForm(),
            'create_invites_form': InvitesForm(),
            'invites': [x for x in Invite.objects.filter(sent=False).order_by('date_created') if not x.expired][:MAX_INVITES],
            'create_location_form': LocationForm(),
            'user': request.user,
            'name': NAME,
            'year': datetime.now(TZ).year,
        })

    return render(request, 'users/index.html', {
        'create_location_form': LocationForm(),
        'user': request.user,
        'name': NAME,
        'year': datetime.now(TZ).year,
    })

def update_author(request, slug, author_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    author = get_object_or_404(Author, id=author_id)

    if request.method == 'GET':
        return render(request, 'articles/update_author.html', {
            'author': author,
            'form': AuthorForm(instance=author),
            'title': 'Update %s' % author.full_name,
            'user': request.user,
            'name': NAME,
            'year': datetime.now(TZ).year,
        })
    elif request.method == 'POST':
        form = AuthorForm(request.POST, request.FILES, instance=author)

        if form.is_valid():
            if 'image' in request.FILES and author.profile_image:
                # only delete image if hash exists and image is not being used elsewhere
                if not Author.objects.filter(
                    ~Q(id=author.id) & (
                        Q(profile_image___image_hash=author.profile_image._image_hash) |
                        Q(profile_image___thumbnail_hash=author.profile_image._image_hash)
                    )
                ) and author.profile_image._image_hash:
                    filename = '%s/authors/%s/%s.jpg' % (MEDIA_ROOT, author.profile_image.date_created.astimezone(TZ).strftime('%Y/%m/%d'), author.profile_image.image_hash)
                    os.remove(filename)

                # only delete thumbnail if hash exists and image is not being used elsewhere
                if Author.objects.filter(
                    ~Q(id=author.id) & (
                        Q(profile_image___image_hash=author.profile_image._thumbnail_hash) |
                        Q(profile_image___thumbnail_hash=author.profile_image._thumbnail_hash)
                    )
                ) and author.profile_image.thumbnail_hash:
                    author.profile_image.thumbnail = None
                else:
                    author.profile_image.thumbnail.delete()

                author.profile_image._image_hash = None
                author.profile_image._thumbnail_hash = None

                author.save()

            updated_author = form.save()

            if 'image' in request.FILES:
                profile_image = AuthorImage.objects.create(image=request.FILES.get('image'))
                profile_image.image_ops()
                profile_image.save()
                updated_author.profile_image = profile_image
            elif form.cleaned_data.get('clear_image'):
                updated_author.profile_image.delete()
                updated_author.profile_image.save()
                updated_author.profile_image = None

            updated_author.save()

            messages.success(request, 'You have successfully updated %s.' % author.full_name)
        else:
            messages.error(request, 'There was an error updating %s.' % author.full_name)

            return render(request, 'home/update_author.html', {
                'author': author,
                'form': form,
                'title': '',
                'user': request.user,
                'name': NAME,
                'year': datetime.now(TZ).year,
            })
    else:
        return HttpResponseBadRequest()

    return HttpResponseRedirect(
        reverse('articles:update-author', args=[slug, author_id])
    )

def delete_author(request, slug, author_id):
    if request.method != 'GET':
        return HttpResponseBadRequest()

    author = get_object_or_404(Author, id=author_id)
    full_name = author.full_name

    try:
        author.delete()
    except OSError:
        messages.error(request, 'There was an issue deleting the specified author.')

        return redirect('users:index')

    punctuation = full_name[-1]
    messages.success(request, 'You have successfully deleted the author named "%s%s"' % (full_name, '' if punctuation == '?' or punctuation == '!' or punctuation == '.' else '.'))

    return redirect('users:index')

def author_autocomplete(request):
    query = request.GET.get('q', '')
    authors = []

    if query == '' or not request.user.is_superuser:
        return render(request, 'home/autocomplete.html', {'authors': []})

    return render(request, 'home/autocomplete.html', {
        'authors': Author.objects.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query)
        ).order_by('last_name')[:5],
    })
