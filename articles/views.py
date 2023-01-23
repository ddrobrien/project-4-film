from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import Post
from .forms import CommentForm


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 3

 
class PostDetail(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'

    def post_detail(request, slug):
        queryset = Post.objects.filter(status=1)
        template_name = 'post_detail.html'
        post = get_object_or_404(Post, slug=slug)
        comments = post.comments.filter(approved=True)
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        new_comment = None
    # Comment posted
        if request.method == 'POST':
            comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
        else:
            comment_form = CommentForm()

        return render(request, "post_detail.html", {
            'post': post,
            'comments': comments,
            'liked': liked,
            'new_comment': new_comment,
            'comment_form': comment_form})
