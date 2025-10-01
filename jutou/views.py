from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Topic, Entry
from .form import TopicForm, EntryForm
from django.http import Http404

def index(request):
    # 渲染首页模板
    return render(request, 'jutou/index.html')

@login_required
def topics(request):
    # 获取按日期降序排列的最近10个主题
    topics = Topic.objects.order_by('-date_added')[:10]
    # 渲染主题列表模板，并传递主题数据
    return render(request, 'jutou/topics.html', {'topics': topics})

@login_required
def topic(request, topic_id):
    # 获取指定ID的主题
    topic = Topic.objects.get(id=topic_id)
    # 获取该主题下按日期降序排列的最近10个条目
    entries = topic.entry_set.order_by('-date_added')[:10]
    # 创建上下文字典，包含主题和条目数据
    context = {'topic': topic, 'entries': entries}
    # 渲染单个主题详情模板，并传递上下文数据
    return render(request, 'jutou/topic.html', context)

@login_required
def new_topic(request):
    # 如果是POST请求，则处理表单数据
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            # 保存表单数据，并重定向到主题列表页面
            form.save()
            return redirect('jutou:topics')
    context = {'form': form}
    return render(request, 'jutou/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    # 获取指定ID的主题
    topic = Topic.objects.get(id=topic_id)
    # 如果是POST请求，则处理表单数据
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(request.POST,request.FILES)
        if form.is_valid():
            # 保存表单数据，并重定向到主题详情页面
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('jutou:topic', topic_id=topic_id)
        else:
            print(form.errors)
    context = {'topic': topic, 'form': form}
    return render(request, 'jutou/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    # 获取指定ID的条目
    entry = Entry.objects.get(id=entry_id)
    # 获取该条目的主题
    topic = entry.topic
    # 如果是POST请求，则处理表单数据
    if request.method != 'POST':
        form = EntryForm(instance=entry)
        form = EntryForm(request.POST,request.FILES, instance=entry)
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            # 保存表单数据，并重定向到主题详情页面
            form.save()
            return redirect('jutou:topic', topic_id=topic.id)
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'jutou/edit_entry.html', context)
# ... 其他视图函数 ...

@login_required
def new_entry(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(request.POST, request.FILES)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.owner = request.user
            new_entry.save()
            return redirect('jutou:topic', topic_id=topic_id)
    context = {'topic': topic, 'form': form}
    return render(request, 'jutou/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic
    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(request.POST, request.FILES, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('jutou:topic', topic_id=topic.id)
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'jutou/edit_entry.html', context)

@login_required
def delete_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic
    if request.user != entry.owner:
        raise Http404("你只能删除你自己的帖子。")
    entry.delete()
    return redirect('jutou:topic', topic_id=entry.topic.id)

@login_required
def delete_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if request.user != topic.owner:
        raise Http404("你只能删除你自己的话题。")
    topic.delete()
    return redirect('jutou:topics')
