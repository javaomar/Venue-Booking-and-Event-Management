from django.shortcuts import redirect 

def user_not_authenticated(function=None, redirect_url ='events:list-events'):


	def decorator(view_func):
		'''
			this decorator checks if the user is authenticated 
			and if so it redirect to events:list-events
		'''
		def wrapped_view(request,*args,**kwargs):
			if request.user.is_authenticated:
				return redirect(redirect_url)

			return view_func(request,*args,**kwargs)

		return wrapped_view


	if function:
		return decorator(function)
	return decorator