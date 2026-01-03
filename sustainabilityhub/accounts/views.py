from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.contrib.auth import get_user_model, login

from django.utils import timezone
from datetime import timedelta
from .forms import CustomUserCreationForm
from .models import UserWarning, OTP
from notifications.utils import create_notification

User = get_user_model()

def otp_login_request(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        
        if not email:
            messages.error(request, 'Please enter your email address.')
            return render(request, 'accounts/otp_login.html')
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email. Please check your email or register.')
            return render(request, 'accounts/otp_login.html')
        
        # Generate OTP
        otp_code = OTP.generate_otp()
        expires_at = timezone.now() + timedelta(minutes=10)
        
        # Delete old OTPs for this email
        OTP.objects.filter(email=email).delete()
        
        # Create new OTP
        OTP.objects.create(
            email=email,
            otp_code=otp_code,
            expires_at=expires_at
        )
        
        # Print OTP to terminal
        print(f'\n{"="*60}')
        print(f'🔐 OTP LOGIN REQUEST')
        print(f'{"="*60}')
        print(f'Email: {email}')
        print(f'OTP Code: {otp_code}')
        print(f'Expires: {expires_at.strftime("%Y-%m-%d %H:%M:%S")}')
        print(f'{"="*60}\n')
        
        request.session['otp_email'] = email
        messages.success(request, f'OTP generated! Check the terminal/console for your OTP code.')
        return redirect('accounts:otp_verify')
    
    return render(request, 'accounts/otp_login.html')

def otp_verify(request):
    email = request.session.get('otp_email')
    otp_type = request.session.get('otp_type', 'login')
    
    if not email:
        messages.error(request, 'Please request an OTP first.')
        return redirect('accounts:otp_login')
    
    if request.method == 'POST':
        otp_code = request.POST.get('otp_code', '').strip()
        
        try:
            otp = OTP.objects.get(email=email, otp_code=otp_code)
            
            if not otp.is_valid():
                messages.error(request, 'OTP has expired or already been used.')
                return render(request, 'accounts/otp_verify.html', {'email': email, 'otp_type': otp_type})
            
            # Mark OTP as used
            otp.is_used = True
            otp.save()
            
            if otp_type == 'reset':
                # Redirect to password reset form
                request.session['reset_email'] = email
                del request.session['otp_email']
                del request.session['otp_type']
                messages.success(request, 'OTP verified! Now set your new password.')
                return redirect('accounts:reset_password')
            else:
                # Log the user in
                user = User.objects.get(email=email)
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                
                # Clear session
                del request.session['otp_email']
                if 'otp_type' in request.session:
                    del request.session['otp_type']
                
                messages.success(request, 'Login successful!')
                return redirect('home')
            
        except OTP.DoesNotExist:
            messages.error(request, 'Invalid OTP code.')
    
    return render(request, 'accounts/otp_verify.html', {'email': email, 'otp_type': otp_type})

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        
        if not email:
            messages.error(request, 'Please enter your email address.')
            return render(request, 'accounts/forgot_password.html')
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email.')
            return render(request, 'accounts/forgot_password.html')
        
        # Generate OTP
        otp_code = OTP.generate_otp()
        expires_at = timezone.now() + timedelta(minutes=10)
        
        # Delete old OTPs for this email
        OTP.objects.filter(email=email).delete()
        
        # Create new OTP
        OTP.objects.create(
            email=email,
            otp_code=otp_code,
            expires_at=expires_at
        )
        
        # Print OTP to terminal
        print(f'\n{"="*60}')
        print(f'🔑 PASSWORD RESET OTP')
        print(f'{"="*60}')
        print(f'Email: {email}')
        print(f'OTP Code: {otp_code}')
        print(f'Expires: {expires_at.strftime("%Y-%m-%d %H:%M:%S")}')
        print(f'{"="*60}\n')
        
        request.session['otp_email'] = email
        request.session['otp_type'] = 'reset'
        messages.success(request, 'OTP generated! Check the terminal for your OTP code.')
        return redirect('accounts:otp_verify')
    
    return render(request, 'accounts/forgot_password.html')

def reset_password(request):
    email = request.session.get('reset_email')
    if not email:
        messages.error(request, 'Invalid password reset session.')
        return redirect('accounts:forgot_password')
    
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/reset_password.html', {'email': email})
        
        if len(password1) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'accounts/reset_password.html', {'email': email})
        
        try:
            user = User.objects.get(email=email)
            user.set_password(password1)
            user.save()
            
            # Clear session
            del request.session['reset_email']
            
            messages.success(request, 'Password reset successful! You can now login with your new password.')
            return redirect('accounts:login')
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return redirect('accounts:forgot_password')
    
    return render(request, 'accounts/reset_password.html', {'email': email})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def admin_users(request):
    from django.db.models import Q, Count
    
    # Get filter parameters
    search = request.GET.get('search', '')
    status_filter = request.GET.get('status', 'all')
    
    # Base queryset with counts
    users = User.objects.annotate(
        warning_count=Count('warnings', filter=Q(warnings__is_active=True)),
        forum_posts_count=Count('forum_posts', distinct=True),
        topics_count=Count('topics', distinct=True),
        created_projects_count=Count('created_projects', distinct=True),
        joined_projects_count=Count('joined_projects', distinct=True)
    ).select_related().order_by('-date_joined')
    
    # Apply search filter
    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search)
        )
    
    # Apply status filter
    if status_filter == 'active':
        users = users.filter(is_active=True, is_superuser=False)
    elif status_filter == 'inactive':
        users = users.filter(is_active=False)
    elif status_filter == 'staff':
        users = users.filter(is_staff=True)
    elif status_filter == 'superuser':
        users = users.filter(is_superuser=True)
    elif status_filter == 'warned':
        users = users.filter(warning_count__gt=0)
    
    # Get statistics
    stats = {
        'total': User.objects.count(),
        'active': User.objects.filter(is_active=True, is_superuser=False).count(),
        'inactive': User.objects.filter(is_active=False).count(),
        'staff': User.objects.filter(is_staff=True).count(),
        'superuser': User.objects.filter(is_superuser=True).count(),
        'warned': User.objects.annotate(
            warning_count=Count('warnings', filter=Q(warnings__is_active=True))
        ).filter(warning_count__gt=0).count(),
    }
    
    return render(request, 'accounts/admin_users.html', {
        'users': users,
        'stats': stats,
        'search': search,
        'status_filter': status_filter
    })

@user_passes_test(lambda u: u.is_superuser)
def create_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, f'User {username} created successfully.')
            return redirect('accounts:admin_users')
    
    return render(request, 'accounts/create_user.html')

@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        if user.is_superuser:
            messages.error(request, 'Cannot delete superuser.')
        else:
            username = user.username
            user.delete()
            messages.success(request, f'User {username} deleted successfully.')
    return redirect('accounts:admin_users')

@user_passes_test(lambda u: u.is_superuser)
def warn_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        warning = UserWarning.objects.create(
            user=user,
            issued_by=request.user,
            severity=request.POST['severity'],
            reason=request.POST['reason'],
            description=request.POST['description']
        )
        
        # Notify user about warning
        create_notification(
            recipient=user,
            notification_type='warning_issued',
            title=f'{warning.get_severity_display()} Warning',
            message=f'Reason: {warning.reason}',
            url='/accounts/my-warnings/'
        )
        
        messages.success(request, f'Warning issued to {user.username}.')
        return redirect('accounts:admin_users')
    
    return render(request, 'accounts/warn_user.html', {'target_user': user})

@user_passes_test(lambda u: u.is_superuser)
def user_warnings(request, pk):
    user = get_object_or_404(User, pk=pk)
    warnings = user.warnings.all()
    return render(request, 'accounts/user_warnings.html', {'target_user': user, 'warnings': warnings})

@user_passes_test(lambda u: u.is_superuser)
def toggle_user_status(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        if user.is_superuser:
            messages.error(request, 'Cannot modify superuser status.')
        else:
            user.is_active = not user.is_active
            user.save()
            status = 'activated' if user.is_active else 'deactivated'
            messages.success(request, f'User {user.username} has been {status}.')
            
            # Notify user about status change
            create_notification(
                recipient=user,
                notification_type='account_status',
                title=f'Account {status.title()}',
                message=f'Your account has been {status} by an administrator.',
                url='/'
            )
    
    return redirect('accounts:admin_users')

from django.contrib.auth.decorators import login_required

@login_required
def my_warnings(request):
    """View for users to see their own warnings"""
    from django.utils import timezone
    
    # Mark all unviewed warnings as viewed
    request.user.warnings.filter(is_active=True, viewed_at__isnull=True).update(viewed_at=timezone.now())
    
    # Get all active warnings
    warnings = request.user.warnings.filter(is_active=True).order_by('-created_at')
    return render(request, 'accounts/my_warnings.html', {'warnings': warnings})

@login_required
def profile(request):
    """View for users to see their own profile"""
    user = request.user
    stats = {
        'topics_count': user.topics.count(),
        'forum_posts_count': user.forum_posts.count(),
        'created_projects_count': user.created_projects.count(),
        'joined_projects_count': user.joined_projects.count(),
        'warnings_count': user.warnings.filter(is_active=True).count(),
    }
    warnings = user.warnings.filter(is_active=True).order_by('-created_at')[:5]
    return render(request, 'accounts/profile.html', {'stats': stats, 'warnings': warnings})

@login_required
def submit_justification(request, pk):
    """Submit justification for a warning"""
    from django.utils import timezone
    warning = get_object_or_404(UserWarning, pk=pk, user=request.user)
    
    if request.method == 'POST':
        justification = request.POST.get('justification', '').strip()
        if justification:
            warning.justification = justification
            warning.justification_submitted_at = timezone.now()
            warning.save()
            messages.success(request, 'Your justification has been submitted.')
            return redirect('accounts:my_warnings')
        else:
            messages.error(request, 'Please provide a justification.')
    
    return render(request, 'accounts/submit_justification.html', {'warning': warning})

@user_passes_test(lambda u: u.is_superuser)
def user_detail(request, pk):
    from django.db.models import Count
    
    user = get_object_or_404(User, pk=pk)
    
    # Get user's content with counts
    topics = user.topics.all()[:10]  # Latest 10 topics
    forum_posts = user.forum_posts.all()[:10]  # Latest 10 posts
    created_projects = user.created_projects.all()[:10]  # Latest 10 created projects
    joined_projects = user.joined_projects.all()[:10]  # Latest 10 joined projects
    warnings = user.warnings.filter(is_active=True)[:10]  # Latest 10 warnings
    
    # Get comprehensive stats
    stats = {
        'topics_count': user.topics.count(),
        'forum_posts_count': user.forum_posts.count(),
        'created_projects_count': user.created_projects.count(),
        'joined_projects_count': user.joined_projects.count(),
        'warnings_count': user.warnings.filter(is_active=True).count(),
        'events_created': user.events_created.count() if hasattr(user, 'events_created') else 0,
        'resources_shared': user.resources_created.count() if hasattr(user, 'resources_created') else 0,
    }
    
    return render(request, 'accounts/user_detail.html', {
        'target_user': user,
        'topics': topics,
        'forum_posts': forum_posts,
        'created_projects': created_projects,
        'joined_projects': joined_projects,
        'warnings': warnings,
        'stats': stats,
    })