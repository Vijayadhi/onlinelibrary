from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect, get_object_or_404

from backend.models import CustomUser, Books, Authors, Categories, IssuseNewBooks
from django.contrib import messages
from django.http import JsonResponse


# Create your views here.
@login_required(login_url='/user_login')
def index(request):
    user = request.user  # Get the current user

    # Count the books that the current user has not returned
    not_returned_books_count = IssuseNewBooks.objects.filter(student=user, is_returned=False).count()

    # Count the books issued to the current user
    issued_books_count = IssuseNewBooks.objects.filter(student=user).count()

    context = {
        "book_list": Books.objects.count(),
        "book_not_returned": not_returned_books_count,
        "issued_books": issued_books_count,
    }

    return render(request, "user/index.html", context)


def perfom_logout(request):
    logout(request)
    return redirect('/')


def user_login(request):
    if (request.method == 'POST'):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_staff:
                return render(request, 'frontend/user_login.html', {'show_admin_popup': True})
            login(request, user)
            return redirect('/index')
    return render(request, "frontend/user_login.html")


def admin_login(request):
    if (request.method == 'POST'):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('/admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials or you are not an admin.')
    return render(request, "frontend/admin_login.html")


@login_required(login_url='/admin_login')
def ad_change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('password')
        new_password = request.POST.get('newpassword')
        confirm_new_password = request.POST.get('confirmpassword')

        if request.user.check_password(current_password):
            if new_password == confirm_new_password:
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)  # Important to update the session

                messages.success(request, 'Password changed successfully.')
                return redirect('/ad_change_password')
            else:
                messages.error(request, 'New password and confirm password do not match.')
        else:
            messages.error(request, 'Current password is incorrect.')
    return render(request, "backend/change_password.html")


def user_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        full_name = request.POST.get('full_name')
        phone_no = request.POST.get('phone_no')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            if CustomUser.objects.filter(username=username, email=email, mobile_no=phone_no).exists():
                return HttpResponse("User with given details already available")

            user = CustomUser.objects.create_user(username=username, email=email, mobile_no=phone_no,
                                                  full_name=full_name, password=password)

            our_student = authenticate(username=username, password=password)
            if our_student is not None:
                login(request, user)
                return redirect('/index')
        else:
            print("Passwords do not match")
            return redirect('/user_signup')

    return render(request, "frontend/use_signup.html")


@login_required(login_url='/admin_login')
def admin_dashboard(request):
    context = {
        "book_list": Books.objects.count(),
        "book_not_returned": IssuseNewBooks.objects.filter(is_returned="False").count(),
        "students": CustomUser.objects.filter(is_staff="False").count(),
        "authors": Authors.objects.count(),
        "categories": Categories.objects.count()
    }
    return render(request, "backend/admin_dashboard.html", context)


@login_required(login_url="/admin_login")
def student_reg(request):
    context = {
        "students": CustomUser.objects.filter(is_staff=False)
    }
    return render(request, "backend/student_reg.html", context)


@login_required(login_url="/admin_login")
def student_detail(request, pk):
    # Retrieve the student using their ID
    student = get_object_or_404(CustomUser, id=pk)

    # Fetch the list of books issued to the student
    issued_books = IssuseNewBooks.objects.filter(student=student)

    context = {
        # 'student': student,
        'issued_books': issued_books,
    }
    return render(request, "backend/student_detail.html", context)


@login_required(login_url="/user_login")
def current_st_detail(request):
    user = request.user  # Get the current user

    # Retrieve the list of issued books for the current user
    issued_books = IssuseNewBooks.objects.filter(student=user)

    context = {
        "issued_books": issued_books,
    }

    return render(request, "backend/user_iss_book.html", context)


@login_required(login_url="admin_login")
def update_status(request, pk):
    student = get_object_or_404(CustomUser, pk=pk)

    if request.method == "POST":
        status = request.POST.get("status")
        student.status = True if status == "true" else False
        student.save()
        return redirect("/student_reg")

    return redirect("/student_reg")


@login_required(login_url='/admin_login')
def add_author(request):
    if request.method == 'POST':
        author_name = request.POST.get('author')
        author = Authors.objects.create(name=author_name)
        author.save()
        messages.error(request, 'Author Added Successfully!')
        return redirect('/add_author')
    else:
        print("Error")
    return render(request, "backend/author/add_author.html")


@login_required(login_url='/admin_login')
def manage_author(request):
    context = {
        "authors": Authors.objects.all()
    }

    return render(request, "backend/author/manage_authors.html", context)


@login_required(login_url='/admin_login')
def update_author(request, pk):
    authors = get_object_or_404(Authors, pk=pk)
    if request.method == 'POST':
        author_name = request.POST.get('author_name')
        authors.name = author_name
        authors.save()
        print("Success")
        return redirect('/manage_author')
    else:
        print("Error")
    context = {'author': authors}
    return render(request, 'backend/author/edit_author.html', context)


@login_required(login_url='/admin_login')
def delete_author(request, pk):
    author = get_object_or_404(Authors, pk=pk)
    if request.method == "POST":
        author.delete()
        return JsonResponse({'message': 'Author deleted successfully.'})
    return redirect('/manage_author')


@login_required(login_url='/admin_login')
def add_category(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        status = request.POST.get('status')
        category = Categories.objects.create(name=category, status=status)
        category.save()
        messages.error(request, 'Category Added Successfully!')
        return redirect('/add_category')
    else:
        print("Error")
    return render(request, "backend/category/add_category.html")


@login_required(login_url='/admin_login')
def manage_category(request):
    context = {
        "category": Categories.objects.all()
    }
    return render(request, "backend/category/manage_category.html", context)


@login_required(login_url='/admin_login')
def update_category(request, pk):
    category = get_object_or_404(Categories, pk=pk)
    if request.method == "POST":
        name = request.POST.get('category_name')  # Use 'category_name' instead of 'name'
        status = request.POST.get('status')  # Retrieve the selected status
        category.name = name
        category.status = status
        category.save()
        # messages.success(request, "Category Updated")  # Use 'messages.success'
        return redirect("/manage_category")

    context = {'category': category}
    return render(request, 'backend/category/edit_category.html', context)


@login_required(login_url='/admin_login')
def delete_category(request, pk):
    category = get_object_or_404(Categories, pk=pk)
    if request.method == "POST":
        category.delete()
        # return JsonResponse({'message': 'Category deleted successfully.'})
    return redirect('/manage_category')


@login_required(login_url='/admin_login')
def add_books(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        isbn_number = request.POST.get('isbn_number')
        price = float(request.POST.get('price'))
        category_id = int(request.POST.get('category'))
        author_id = int(request.POST.get('author'))

        category = Categories.objects.get(pk=category_id)
        author = Authors.objects.get(pk=author_id)

        image_file = request.FILES.get('bookpic')

        new_book = Books(name=name, isbn_number=isbn_number, price=price,
                         category=category, author=author, image=image_file)
        new_book.save()

        return redirect('/manage_books')

    categories = Categories.objects.all()
    authors = Authors.objects.all()

    context = {'categories': categories, 'authors': authors}
    return render(request, 'backend/books/add_book.html', context)


@login_required(login_url='/admin_login')
def manage_books(request):
    context = {
        "book_list": Books.objects.all()
    }
    return render(request, "backend/books/manage_books.html", context)


@login_required(login_url='/admin_login')
def update_book(request, pk):
    book = get_object_or_404(Books, pk=pk)
    update_successful = False

    if request.method == 'POST':
        # Extract the form data
        name = request.POST.get('name')
        isbn_number = request.POST.get('isbn_number')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        author_id = request.POST.get('author')
        image_file = request.FILES.get('bookpic')

        # Update the book object with the new data
        book.name = name
        book.isbn_number = isbn_number
        book.price = price
        book.category_id = category_id
        book.author_id = author_id

        # Handle the image update (if provided)
        if image_file:
            book.image = image_file

        book.save()
        print("Success")
        # update_successful = True
        return redirect('/manage_books')

    # Pass the book object in the context dictionary to prefill the form fields
    context = {'book': book}
    return render(request, 'backend/books/edit_books.html', context)


@login_required(login_url='/admin_login')
def delete_book(request, pk):
    book = get_object_or_404(Books, pk=pk)

    if request.method == 'POST':
        book.delete()
        # If the book is successfully deleted, return a JSON response
        # to indicate the success to the frontend
        return JsonResponse({'message': 'Book deleted successfully.'})

    # If the request method is not POST, render the confirmation page
    return redirect('/manage_books')


@login_required(login_url='/admin_login')
def issue_new_book(request):
    students = CustomUser.objects.filter(is_staff=False)  # Get non-staff students
    books = Books.objects.filter(is_issued=False)

    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        book_id = request.POST.get('book_id')

        student = CustomUser.objects.get(id=student_id)
        book = Books.objects.get(id=book_id)

        new_issue_book = IssuseNewBooks(student=student, books=book)
        new_issue_book.save()

        return redirect('/manage_issued')

    context = {'students': students, 'books': books}
    return render(request, "backend/issue_books/issue_new_book.html", context)


@login_required(login_url='/admin_login')
def manage_issued_books(request):
    context = {
        "manage_issued": IssuseNewBooks.objects.all()
    }
    return render(request, "backend/issue_books/manage_issued_books.html", context)


@login_required(login_url='/admin_login')
def update_issued_book(request, pk):
    issued_book = get_object_or_404(IssuseNewBooks, pk=pk)
    context = {'issued_book': issued_book}

    # If the book is not returned, process the update
    if not issued_book.is_returned:
        if request.method == 'POST':
            fine = float(request.POST.get('fine'))

            # Update the book's fine and status
            issued_book.fine = fine
            issued_book.is_returned = True
            issued_book.save()

            # Set the corresponding book's is_issued to False
            issued_book.books.is_issued = False
            issued_book.books.save()
            return redirect('/manage_issued')  # Redirect to the list of issued books

        return render(request, 'backend/issue_books/update_issued.html', context)

    # If the book is already returned, just show the details
    return render(request, 'backend/issue_books/update_issued.html', context)


@login_required(login_url="/user_login")
def list_books(request):
    context = {
        "books": Books.objects.all()
    }
    return render(request, 'user/book_list.html', context)


@login_required(login_url="/user_login")
def profile(request):
    user = request.user  # Get the current user

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        mobile_no = request.POST.get('mobile_no')

        # Update the user's profile fields
        user.full_name = full_name
        user.mobile_no = mobile_no
        user.save()
        messages.success(request, "Profile Updated Successfully")

    context = {
        "user": user,
    }

    return render(request, "user/profile.html", context)


@login_required(login_url="/user_login")
def user_change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('password')
        new_password = request.POST.get('newpassword')
        confirm_new_password = request.POST.get('confirmpassword')

        if request.user.check_password(current_password):
            if new_password == confirm_new_password:
                request.user.set_password(new_password)
                request.user.save()
                messages.success(request, 'Password changed successfully.')

                update_session_auth_hash(request, request.user)  # Important to update the session

                return redirect('/ad_change_password')
            else:
                messages.error(request, 'New password and confirm password do not match.')

        else:
            messages.error(request, 'Current password is incorrect.')
    return render(request, "user/user_change_password.html")
