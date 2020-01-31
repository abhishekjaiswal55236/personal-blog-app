from django.shortcuts import render,redirect,get_object_or_404

# Create your views here.
from django.http import HttpResponse,Http404
from .models import Board,Topic,Post
from django.contrib.auth.models import User
from .forms import NewTopicForm,PostForm
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView
from django.utils import timezone
from django.views.generic import ListView
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
#for model you can use list view
class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'boards/home.html'



def board_topics(request,board_name):

    board = Board.objects.get(name= board_name)
    queryset = board.topics.order_by("-last_update")
    page = request.GET.get('page',1)
    paginator = Paginator(queryset,10)

    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)

    return render(request,'boards/topics.html',{'board':board,'topics':topics})


def about(request):
    return render(request,'boards/about.html')


@login_required
def new_topic(request,board_name):
    try:
        board = Board.objects.get(name=board_name)
    except:
        raise Http404


    if request.method == 'POST':

        user = User.objects.first()        #to get currently logged in user 


        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.stater = request.user
            topic.save()
            post = Post.objects.create(
                message = form.cleaned_data.get('message'),
                topic = topic,
                author = request.user
            )


            return redirect('board_topics',board.name)
    else:
        form = NewTopicForm()
    return render(request,'new_topic.html',{'board':board,'form':form})

def post_list(request,board_name,topic_id):
    board = Board.objects.get(name=board_name)
    topic = get_object_or_404(Topic , board=board ,pk=topic_id)
    topic.views+=1
    topic.save()
    return render(request , 'post_list.html',{'topic':topic})


@login_required
def reply_topic(request,board_name ,topic_id):
    board = Board.objects.get(name=board_name)
    topic = get_object_or_404(Topic , board=board ,pk=topic_id)

    if request.method=="POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.author = request.user
            post.save()
            return redirect('post_list',board_name=board_name,topic_id=topic_id)
    else:
        form = PostForm()
    return render(request , 'reply_topic.html',{'topic':topic , 'form':form } )



class PostUpdateView(UpdateView):
    model = Post

    fields = ('message',)

    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'


    def form_valid(self,form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.update_date = timezone.now()
        post.save()
        return redirect('post_list',board_name=post.topic.board,topic_id=post.topic.pk)


