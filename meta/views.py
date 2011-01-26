# -*- coding: utf-8 -*-

from meta.models import *
from meta.forms import *
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator, InvalidPage, EmptyPage
import operator
from itis import Itis

# Main
def main_page(request):
    '''Página principal mostrando destaques e pontos de partida para navegar.'''
    #TODO Deixar página mais atrativa e eficiente.
    # Tenta encontrar destaques.
    images = Image.objects.filter(highlight=True, is_public=True).order_by('?')
    if not images:
        images = Image.objects.filter(is_public=True).order_by('?')
    if not images:
        images = ['']
    image = images[0]
    if images[0] != '':
        # Retira imagem principal da lista de destaques.
        thumbs = images.exclude(id=image.id)[:4]
    else:
        thumbs = []
    # Tenta encontrar destaques.
    videos = Video.objects.filter(highlight=True, is_public=True).order_by('?')
    if not videos:
        videos = Video.objects.filter(is_public=True).order_by('?')
    if not videos:
        videos = ['']
    video = videos[0]
    tags = Tag.objects.all()
    locations = Sublocation.objects.all()
    variables = RequestContext(request, {
        'image': image,
        'thumbs': thumbs,
        'video': video,
        'tags': tags,
        'locations': locations,
        })
    return render_to_response('main_page.html', variables)

def search_page(request):
    '''Página de busca com um formulário simples.
    
    Procura termo no campo tsv do banco de dados, que possibilita o full-text search.
    '''
    #TODO Implementar jQuery e AJAX para melhorar usabilidade.
    form = SearchForm()

    # Refinamentos.
    queries = {
            u'query': '',
            u'author': [],
            u'tag': [],
            u'size': [],
            u'taxon': [],
            u'sublocation': [],
            u'city': [],
            u'state': [],
            u'country': [],
            }

    image_list = []
    video_list = []
    images = []
    videos = []
    show_results = False

    if 'query' in request.GET or 'author' in request.GET or 'size' in request.GET or 'tag' in request.GET or 'taxon' in request.GET or 'sublocation' in request.GET or 'city' in request.GET or 'state' in request.GET or 'country' in request.GET:
        show_results = True
        # Query
        if 'query' in request.GET:
            #TODO Lidar com queries no novo sistema de refinamento.
            query = request.GET['query'].strip()
            # Faz full-text search no banco de dados, usando o campo tsv.
            image_queryset = Image.objects.extra(
                    select={
                        'rank': "ts_rank_cd(tsv, plainto_tsquery('portuguese', %s), 32)",
                        },
                    where=["tsv @@ plainto_tsquery('portuguese', %s)"],
                    params=[query],
                    select_params=[query, query],
                    order_by=('-rank',)
                    )
            video_queryset = Video.objects.extra(
                    select={
                        'rank': "ts_rank_cd(tsv, plainto_tsquery('portuguese', %s), 32)",
                        },
                    where=["tsv @@ plainto_tsquery('portuguese', %s)"],
                    params=[query],
                    select_params=[query, query],
                    order_by=('-rank',)
                    )
            image_list = image_queryset.exclude(is_public=False)
            video_list = video_queryset.exclude(is_public=False) 
            form = SearchForm({'query': query})
            queries['query'] = query

        # Author
        if 'author' in request.GET:
            authors = request.GET['author'].split(',')
            queries['author'] = Author.objects.filter(slug__in=authors)
            if image_list and video_list:
                for author in authors:
                    image_list = image_list.filter(author__slug=author)
                    video_list = video_list.filter(author__slug=author)
            else:
                for author in authors:
                    if image_list and video_list:
                        image_list = image_list.filter(author__slug=author)
                        video_list = video_list.filter(author__slug=author)
                    else:
                        image_list = Image.objects.filter(author__slug=author)
                        video_list = Video.objects.filter(author__slug=author)

        # Tag 
        if 'tag' in request.GET:
            tags = request.GET['tag'].split(',')
            queries['tag'] = Tag.objects.filter(slug__in=tags)
            if image_list and video_list:
                for tag in tags:
                    image_list = image_list.filter(tag__slug=tag)
                    video_list = video_list.filter(tag__slug=tag)
            else:
                for tag in tags:
                    if image_list and video_list:
                        image_list = image_list.filter(tag__slug=tag)
                        video_list = video_list.filter(tag__slug=tag)
                    else:
                        image_list = Image.objects.filter(tag__slug=tag)
                        video_list = Video.objects.filter(tag__slug=tag)

        # Size
        if 'size' in request.GET:
            size = request.GET['size']
            queries['size'] = Size.objects.filter(id=size)
            if image_list and video_list:
                image_list = image_list.filter(size=size)
                video_list = video_list.filter(size=size)
            else:
                image_list = Image.objects.filter(size=size)
                video_list = Video.objects.filter(size=size)

        # Taxon
        if 'taxon' in request.GET:
            taxa = request.GET['taxon'].split(',')
            queries['taxon'] = Taxon.objects.filter(slug__in=taxa)
            if image_list and video_list:
                for taxon in taxa:
                    image_list = image_list.filter(taxon__slug=taxon)
                    video_list = video_list.filter(taxon__slug=taxon)
            else:
                for taxon in taxa:
                    if image_list and video_list:
                        image_list = image_list.filter(taxon__slug=taxon)
                        video_list = video_list.filter(taxon__slug=taxon)
                    else:
                        image_list = Image.objects.filter(taxon__slug=taxon)
                        video_list = Video.objects.filter(taxon__slug=taxon)

        # Sublocation
        if 'sublocation' in request.GET:
            sublocations = request.GET['sublocation'].split(',')
            queries['sublocation'] = Sublocation.objects.filter(slug__in=sublocations)
            if image_list and video_list:
                for sublocation in sublocations:
                    image_list = image_list.filter(
                            sublocation__slug=sublocation)
                    video_list = video_list.filter(
                            sublocation__slug=sublocation)
            else:
                for sublocation in sublocations:
                    if image_list and video_list:
                        image_list = image_list.filter(
                                sublocation__slug=sublocation)
                        video_list = video_list.filter(
                                sublocation__slug=sublocation)
                    else:
                        image_list = Image.objects.filter(
                                sublocation__slug=sublocation)
                        video_list = Video.objects.filter(
                                sublocation__slug=sublocation)

        # City
        if 'city' in request.GET:
            cities = request.GET['city'].split(',')
            queries['city'] = City.objects.filter(slug__in=cities)
            if image_list and video_list:
                for city in cities:
                    image_list = image_list.filter(city__slug=city)
                    video_list = video_list.filter(city__slug=city)
            else:
                for city in cities:
                    if image_list and video_list:
                        image_list = image_list.filter(city__slug=city)
                        video_list = video_list.filter(city__slug=city)
                    else:
                        image_list = Image.objects.filter(city__slug=city)
                        video_list = Video.objects.filter(city__slug=city)

        # State
        if 'state' in request.GET:
            states = request.GET['state'].split(',')
            queries['state'] = State.objects.filter(slug__in=states)
            if image_list and video_list:
                for state in states:
                    image_list = image_list.filter(state__slug=state)
                    video_list = video_list.filter(state__slug=state)
            else:
                for state in states:
                    if image_list and video_list:
                        image_list = image_list.filter(state__slug=state)
                        video_list = video_list.filter(state__slug=state)
                    else:
                        image_list = Image.objects.filter(state__slug=state)
                        video_list = Video.objects.filter(state__slug=state)

        # Country
        if 'country' in request.GET:
            countries = request.GET['country'].split(',')
            queries['country'] = Country.objects.filter(slug__in=countries)
            if image_list and video_list:
                for country in countries:
                    image_list = image_list.filter(country__slug=country)
                    video_list = video_list.filter(country__slug=country)
            else:
                for country in countries:
                    if image_list and video_list:
                        image_list = image_list.filter(country__slug=country)
                        video_list = video_list.filter(country__slug=country)
                    else:
                        image_list = Image.objects.filter(country__slug=country)
                        video_list = Video.objects.filter(country__slug=country)

        images = get_paginated(request, image_list)
        videos = get_paginated(request, video_list)
    variables = RequestContext(request, {
        'form': form,
        'images': images,
        'videos': videos,
        'image_list': image_list,
        'video_list': video_list,
        'show_results': show_results,
        'queries': queries,
        })
    return render_to_response('buscar.html', variables)

def org_page(request):
    '''Página mostrando a organização dos metadados.

    Além de buscar as descrições de cada categoria, mostra exemplos aleatórios de imagens.
    '''
    # Tamanhos
    sizes = Size.objects.all().order_by('position')
    # Técnicas
    tecnica = TagCategory.objects.get(name=u'Técnica')
    microscopia = TagCategory.objects.get(name=u'Microscopia')
    # Estágios
    estagio = TagCategory.objects.get(name=u'Estágio de vida')
    tmp = ['','','','','']
    for fase in estagio.tags.all():
        if fase.name == 'gameta':
            tmp[0] = fase
        elif fase.name == 'embrião':
            tmp[1] = fase
        elif fase.name == 'larva':
            tmp[2] = fase
        elif fase.name == 'juvenil':
            tmp[3] = fase
        elif fase.name == 'adulto':
            tmp[4] = fase
    estagios = tmp
    # Modos
    pelagicos = TagCategory.objects.get(name=u'Pelágicos')
    bentonicos = TagCategory.objects.get(name=u'Bentônicos')
    # Habitat
    habitat = TagCategory.objects.get(name=u'Habitat')
    # Diversos 
    diversos = TagCategory.objects.get(name=u'Diversos')
    variables = RequestContext(request, {
        'sizes': sizes,
        'microscopia': microscopia,
        'tecnica': tecnica,
        'estagios': estagios,
        'estagio': estagio,
        'pelagicos': pelagicos,
        'bentonicos': bentonicos,
        'habitat': habitat,
        'diversos': diversos,
        'title': u'Organização do banco',
        })
    return render_to_response('organizacao.html', variables)

def hidden_page(request):
    '''Página mostrando imagens não públicas.

    Usada pelos administradores como referência para a edição de metadados.
    '''
    images = Image.objects.filter(is_public=False)
    videos = Video.objects.filter(is_public=False)
    variables = RequestContext(request, {
        'images': images,
        'videos': videos,
        })
    return render_to_response('hidden.html', variables)

def feedback_page(request):
    '''Montada para receber o feedback dos usuários durante os testes.'''
    variables = RequestContext(request, {})
    return render_to_response('feedback.html', variables)

def fixtaxa_page(request):
    '''Página mostrando táxons sem pai.'''
    invalids = []
    valids = []
    if request.method == 'POST':
        form = FixTaxaForm(request.POST)
        if form.is_valid():
            for name in form.cleaned_data['revise']:
                try:
                    taxon = Itis(name)
                    if taxon.hierarchy:
                        valids.append(name)
                    else:
                        try:
                            # Gambiarra para encontrar gêneros nas tabelas.
                            genus = name.split()[0]
                            taxon = Itis(genus)
                            if taxon.hierarchy:
                                try:
                                    genus, new = Taxon.objects.get_or_create(name=genus)
                                    for parent in taxon.parents:
                                        newtaxon, new = Taxon.objects.get_or_create(name=parent.taxonName)
                                        if new:
                                            newtaxon.rank = parent.rankName
                                            newtaxon.tsn = parent.tsn
                                            if parent.parentName:
                                                newtaxon.parent = Taxon.objects.get(name=parent.parentName)
                                            newtaxon.save()
                                            print u'Salvo!'
                                        else:
                                            print u'Já existe!'

                                    if taxon.parent_name:
                                        genus.parent = Taxon.objects.get(name=taxon.parent_name)
                                    if taxon.tsn:
                                        genus.tsn = taxon.tsn
                                    if taxon.rank:
                                        genus.rank = taxon.rank
                                except:
                                    print u'Não rolou pegar hierarquia...'
                                genus.save()
                                binomial = Taxon.objects.get(name=name)
                                binomial.parent = genus
                                binomial .save()
                                valids.append(name.split()[0])
                            else:
                                invalids.append(name.split()[0])
                        except:
                            invalids.append(name)
                except:
                    invalids.append(name)
    else:
        form = FixTaxaForm()
    variables = RequestContext(request, {
        'form': form,
        'invalids': invalids,
        'valids': valids,
        })
    return render_to_response('fixtaxa.html', variables)

def all_page(request):
    '''Página todas as imagens do site.'''
    image_list = Image.objects.filter(is_public=True).order_by('?')
    video_list = Video.objects.filter(is_public=True).order_by('?')
    images = get_paginated(request, image_list)
    videos = get_paginated(request, video_list)
    variables = RequestContext(request, {
        'images': images,
        'videos': videos,
        })
    return render_to_response('tudo.html', variables)

# Single
def image_page(request, image_id):
    '''Página única de cada imagem com todas as informações.'''
    if request.method == 'POST':
        form = RelatedForm(request.POST)
        if form.is_valid:
            related = form.data['type']
            request.session['rel_type'] = form.data['type']
    else:
        try:
            form = RelatedForm(initial={'type': request.session['rel_type']})
            related = request.session['rel_type']
        except:
            form = RelatedForm(initial={'type': 'author'})
            related = u'author'
    image = get_object_or_404(Image, id=image_id)
    #TODO Checar sessão para evitar overdose de views
    image.view_count = image.view_count + 1
    image.save()
    tags = image.tag_set.all().order_by('name')
    references = image.reference_set.all().order_by('-citation')
    variables = RequestContext(request, {
        'media': image,
        'tags': tags,
        'references': references,
        'form': form,
        'related': related,
        })
    return render_to_response('media_page.html', variables)

def video_page(request, video_id):
    '''Página única de cada vídeo com todas as informações.'''
    if request.method == 'POST':
        form = RelatedForm(request.POST)
        if form.is_valid:
            related = form.data['type']
            request.session['rel_type'] = form.data['type']
    else:
        try:
            form = RelatedForm(initial={'type': request.session['rel_type']})
            related = request.session['rel_type']
        except:
            form = RelatedForm(initial={'type': 'author'})
            related = u'author'
    video = get_object_or_404(Video, id=video_id)
    #TODO Checar sessão para evitar overdose de views
    video.view_count = video.view_count + 1
    video.save()
    tags = video.tag_set.all().order_by('name')
    references = video.reference_set.all().order_by('-citation')
    variables = RequestContext(request, {
        'media': video,
        'tags': tags,
        'references': references,
        'form': form,
        'related': related,
        })
    return render_to_response('media_page.html', variables)

def meta_page(request, model_name, field, slug):
    '''Página de um metadado.

    Mostra galeria com todas as imagens que o possuem.
    '''
    queries = {
            u'query': '',
            u'author': [],
            u'tag': [],
            u'size': [],
            u'taxon': [],
            u'sublocation': [],
            u'city': [],
            u'state': [],
            u'country': [],
            }
    qmodels = model_name.objects.filter(slug__in=[slug])
    queries[field] = qmodels
    model = get_object_or_404(model_name, slug=slug)
    filter_args = {field: model}
    try:
        q = [Q(**filter_args),]
        q = recurse(model, q)
        image_list = Image.objects.filter(reduce(operator.or_,
            q)).exclude(is_public=False).distinct().order_by('-id')
        video_list = Video.objects.filter(reduce(operator.or_,
            q)).exclude(is_public=False).distinct().order_by('-id')
    except:
        image_list = Image.objects.filter(**filter_args).exclude(is_public=False).distinct().order_by('-id')
        video_list = Video.objects.filter(**filter_args).exclude(is_public=False).distinct().order_by('-id')
    images = get_paginated(request, image_list)
    videos = get_paginated(request, video_list)
    variables = RequestContext(request, {
        'images': images,
        'videos': videos,
        'image_list': image_list,
        'video_list': video_list,
        'meta': model,
        'field': field,
        'queries': queries,
        })
    return render_to_response('meta_page.html', variables)

# Lists
def meta_list_page(request, model, plural):
    '''Lista com todos os metadados.
    
    Não utilizado?
    '''
    objects = model.objects.order_by('name')
    variables = RequestContext(request, {
        'metas': objects,
        'plural': plural,
        })
    return render_to_response('meta_list_page.html', variables)

# Menu
def taxa_page(request):
    '''Página mostrando grupos taxonômicos de maneira organizada.'''
    variables = RequestContext(request, {
        })
    return render_to_response('taxa_page.html', variables)

def places_page(request):
    '''Página mostrando locais de maneira organizada.'''
    sublocations = Sublocation.objects.order_by('name')
    cities = City.objects.order_by('name')
    states = State.objects.order_by('name')
    countries = Country.objects.order_by('name')
    variables = RequestContext(request, {
        'sublocations': sublocations,
        'cities': cities,
        'states': states,
        'countries': countries,
        })
    return render_to_response('places_page.html', variables)

def tags_page(request):
    '''Página mostrando tags organizados por categoria.'''
    tags = Tag.objects.order_by('parent')
    sizes = Size.objects.order_by('id')
    variables = RequestContext(request, {
        'tags': tags,
        'sizes': sizes,
        })
    return render_to_response('tags_page.html', variables)

def authors_page(request):
    '''Página mostrando autores e especialistas.'''
    authors = Author.objects.order_by('name')
    sources = Source.objects.order_by('name')
    variables = RequestContext(request, {
        'authors': authors,
        'sources': sources,
        })
    return render_to_response('authors_page.html', variables)

def refs_page(request):
    '''Página mostrando referências.'''
    references = Reference.objects.order_by('-citation')
    variables = RequestContext(request, {
        'references': references,
        })
    return render_to_response('refs_page.html', variables)

# Internal functions
def get_paginated(request, obj_list, n_page=16):
    '''Retorna o Paginator de um queryset.'''
    paginator = Paginator(obj_list, n_page)
    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    # If page request (9999) is out of range, deliver last page of results.
    try:
        obj = paginator.page(page)
    except (EmptyPage, InvalidPage):
        obj = paginator.page(paginator.num_pages)
    return obj

def recurse(taxon, q=None):
    '''Recursivamente retorna todos os táxons-filho em um Q object.'''
    #TODO Usar mptt para agilizar.
    if not q:
        q = []
    if taxon.children.all():
        for child in taxon.children.all():
            q.append(Q(**{'taxon': child}))
            recurse(child, q)
    return q
