from django.shortcuts import render, redirect, get_object_or_404
from .models import Job, Applicants, Selected
from Candidates.models import Profile, Skill
from .forms import NewJobForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib import messages
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
def cosine_similarity(X , Y ): 
    # tokenization
    X_list = word_tokenize(X) 
    Y_list = word_tokenize(Y)
    
    # sw contains the list of stopwords
    sw = stopwords.words('english') 
    l1 =[];l2 =[]
    
    # remove stop words from the string
    X_set = {w for w in X_list if not w in sw} 
    Y_set = {w for w in Y_list if not w in sw}

    # form a set containing keywords of both strings 
    rvector = X_set.union(Y_set) 
    for w in rvector:
        if w in X_set: l1.append(1) # create a vector
        else: l1.append(0)
        if w in Y_set: l2.append(1)
        else: l2.append(0)
    c = 0
    
    # cosine formula 
    for i in range(len(rvector)):
            c+= l1[i]*l2[i]
    cosine = c / float((sum(l1)*sum(l2))**0.5)
    return cosine
        


def rec_details(request):
    context = {
        'rec_home_page': "active",
        'rec_navbar': 1,
    }
    return render(request, 'recruiters/details.html', context)


@login_required
def add_job(request):
    user = request.user
    if request.method == "POST":
        form = NewJobForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.recruiter = user
            data.save()
            return redirect('job-list')
    else:
        form = NewJobForm()
    context = {
        'add_job_page': "active",
        'form': form,
        'rec_navbar': 1,
    }
    return render(request, 'recruiters/add_job.html', context)


@login_required
def edit_job(request, slug):
    user = request.user
    job = get_object_or_404(Job, slug=slug)
    if request.method == "POST":
        form = NewJobForm(request.POST, instance=job)
        if form.is_valid():
            data = form.save(commit=False)
            data.save()
            return redirect('add-job-detail', slug)
    else:
        form = NewJobForm(instance=job)
    context = {
        'form': form,
        'rec_navbar': 1,
        'job': job,
    }
    return render(request, 'recruiters/edit_job.html', context)


@login_required
def job_detail(request, slug):
    job = get_object_or_404(Job, slug=slug)
    context = {
        'job': job,
        'rec_navbar': 1,
    }
    return render(request, 'recruiters/job_detail.html', context)


@login_required
def all_jobs(request):
    jobs = Job.objects.filter(recruiter=request.user).order_by('-date_posted')
    paginator = Paginator(jobs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'manage_jobs_page': "active",
        'jobs': page_obj,
        'rec_navbar': 1,
    }
    return render(request, 'recruiters/job_posts.html', context)


@login_required
def search_candidates(request):
    profile_list = Profile.objects.all()
    profiles = []
    for profile in profile_list:
        if profile.user != request.user:
            profiles.append(profile)
    rec1 = request.GET.get('r')
    rec2 = request.GET.get('s')
    rec4 = request.GET.get('bio')
    rec3 = request.GET.get('sk')

    if rec1 == None or rec1== '' :
        li1 = Profile.objects.all()
    else:
        li1 = Profile.objects.filter(location__icontains=rec1)


    if rec2 == None or rec2=='':
        li2 = Profile.objects.all()
    else:
        li2= [ ] 
        print(":55",  rec2)
        u = User.objects.filter(experience_level__icontains=rec2)
        print("u", u)
        for x in u: 
            li2.append(Profile.objects.get(user =x))
    if rec3 == None or rec3=="" :
        li3 = Profile.objects.all()
    else:
        print("112244", rec3)

        x = Skill.objects.filter(skill__icontains=rec3)  
        li3 =[]
        for i in x.values() :

            li3.append(Profile.objects.get(user_id=i["user_id"] ) )
    if rec4 == None or rec4== '': 
        li4= Profile.objects.all()
        print("6666666")
    else: 
        li4= [ ]
        X= rec4 
        for u in User.objects.all():
            Y = u.bio
            similarity = cosine_similarity(X , Y)
            if similarity>=.3 : 
                li4.append(Profile.objects.filter(user= u).first())
                
                   

    print("1" ,li1)
    print("2" ,li2)
    print("3", li3)
    print("4" ,  li4)
    final = []
    profiles_final = []

    for i in li1:
        if i in li2 and  i in li3  and i  in  li4 :
            final.append(i)
    for i in final:
        if i in profiles:
            profiles_final.append(i)
    
    paginator = Paginator(profiles_final, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print("f",profiles_final)
    context = {
        'search_candidates_page': "active",
        'rec_navbar': 1,
        'profiles': page_obj,
    }
    
    return render(request, 'recruiters/candidate_search.html', context)


@login_required
def job_candidate_search(request, slug):
    job = get_object_or_404(Job, slug=slug)
    relevant_candidates = []
    common = []
    applicants = Profile.objects.filter(looking_for=job.job_type)
    job_skills = []
    skills = str(job.skills_req).split(",")
    for skill in skills:
        job_skills.append(skill.strip().lower())
    for applicant in applicants:
        user = applicant.user
        skill_list = list(Skill.objects.filter(user=user))
        skills = []
        for i in skill_list:
            skills.append(i.skill.lower())
        common_skills = list(set(job_skills) & set(skills))
        if (len(common_skills) != 0 ):
            relevant_candidates.append(applicant)
            common.append(len(common_skills))
    objects = zip(relevant_candidates, common)
    objects = sorted(objects, key=lambda t: t[1], reverse=True)
    objects = objects[:100]
    context = {
        'rec_navbar': 1,
        'job': job,
        'objects': objects,
        'job_skills': len(job_skills),
        'relevant': len(relevant_candidates),

    }
    return render(request, 'recruiters/job_candidate_search.html', context)


@login_required
def applicant_list(request, slug):
    job = get_object_or_404(Job, slug=slug)
    applicants = Applicants.objects.filter(job=job).order_by('date_posted')
    profiles = []
    for applicant in applicants:
        profile = Profile.objects.filter(user=applicant.applicant).first()
        profiles.append(profile)
    context = {
        'rec_navbar': 1,
        'profiles': profiles,

        'job': job,
    }
    return render(request, 'recruiters/applicant_list.html', context)


@login_required
def selected_list(request, slug):
    job = get_object_or_404(Job, slug=slug)
    selected = Selected.objects.filter(job=job).order_by('date_posted')
    profiles = []
    for applicant in selected:
        profile = Profile.objects.filter(user=applicant.applicant).first()
        profiles.append(profile)
    context = {
        'rec_navbar': 1,
        'profiles': profiles,
        'job': job,
    }
    return render(request, 'recruiters/selected_list.html', context)


@login_required
def select_applicant(request, can_id, job_id):
    job = get_object_or_404(Job, slug=job_id)
    profile = get_object_or_404(Profile, slug=can_id)
    user = profile.user
    selected, created = Selected.objects.get_or_create(job=job, applicant=user)
    applicant = Applicants.objects.filter(job=job, applicant=user).first()
    applicant.delete()
    return HttpResponseRedirect('/hiring/job/{}/applicants'.format(job.slug))


@login_required
def remove_applicant(request, can_id, job_id):
    job = get_object_or_404(Job, slug=job_id)
    profile = get_object_or_404(Profile, slug=can_id)
    user = profile.user
    applicant = Applicants.objects.filter(job=job, applicant=user).first()
    applicant.delete()
    return HttpResponseRedirect('/hiring/job/{}/applicants'.format(job.slug))
