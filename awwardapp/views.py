from django.shortcuts import render,redirect,get_object_or_404
from .models import Project,Profile,Comments
from django.http  import HttpResponse,Http404
from django.contrib.auth.decorators import login_required
from .forms import NewProfileForm,NewProjectForm,commentForm, RateForm
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response
from .serialiser import ProfileSerializer,ProjectSerializer

# Create your views here.

def welcome(request):
    all_projects = Project.get_all_projects()
    awwardapp_users = Profile.get_all_awwardproj_users()
    current_user = request.user
    rate_form = RateForm()
    # myprof = Profile.objects.filter(id = current_user.id).first()
    # mycomm = Comments.objects.filter(id = current_user.id).first()
    return render(request, 'welcome.html', {"all_projects":all_projects, "awwardapp_users":awwardapp_users, 'rate_form':rate_form})


@login_required(login_url='/accounts/login/')
def my_profile(request):

    current_user = request.user
    profi_images = Project.objects.filter(user = current_user)
    my_profile = Profile.objects.filter(user = current_user).first()
    return render(request, 'profile.html', {"profi_images":profi_images, "my_profile":my_profile})


@login_required(login_url='/accounts/login/')
def add_profile(request):
    current_user = request.user
    profile = Profile.objects.filter(id = current_user.id)
    if request.method == 'POST':
        form = NewProfileForm(request.POST, request.FILES)
        if form.is_valid():
            caption = form.save(commit=False)
            caption.user = current_user
            caption.save()
            return redirect('myprofile')

    else:
        form = NewProfileForm()
    return render(request, 'edit_profile.html', {"form": form})


def search_users(request):
  if 'username' in request.GET and request.GET["username"]:
      search_term = request.GET.get("username")
      searched_users = Profile.search_by_profile(search_term)
      message = f"{search_term}"
      return render(request, "search.html",{"message":message,"users": searched_users})
  else:
      message = "You haven't searched for any term"
      return render(request, 'search.html',{"message":message})


@login_required(login_url='/accounts/login/')
def upload_image(request):

    current_user = request.user
    if request.method == 'POST':
        form = NewProjectForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = current_user
            image.save()
        return redirect('welcome')

    else:
        form = NewProjectForm()
    return render(request, 'upload.html', {"form": form})


@login_required(login_url='/accounts/login/')
def add_comment(request, project_id):
    current_user = request.user
    project_item = Project.objects.filter(id = project_id).first()
    profiles = Profile.objects.filter( user = current_user.id).first()
    if request.method == 'POST':
        form = commentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.posted_by = profiles
            comment.commented_project = project_item
            comment.save()
            return redirect('welcome')

    else:
        form = commentForm()
    return render(request, 'comment_form.html', {"form": form, "project_id": project_id})


def rating(request,rate_id):

    current_user = request.user
    project = get_object_or_404(Project,pk=rate_id)
    if request.method == 'POST':
        rate_form = RateForm(request.POST, request.FILES)
        if rate_form.is_valid():
            rate = rate_form.save(commit=False)
            rate.project = project
            rate.rater = current_user
            rate.save()
        return redirect('welcome')

    return render(request, 'welcome.html')



class ProfileList(APIView):
    def get(self, request, format=None):
        all_users = Profile.objects.all()
        serializers = ProfileSerializer(all_users, many=True)
        return Response(serializers.data)

class ProjectList(APIView):
    def get(self, request, format=None):
        all_projects = Project.objects.all()
        serializers = ProjectSerializer(all_projects, many=True)
        return Response(serializers.data)