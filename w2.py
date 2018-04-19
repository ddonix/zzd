import web
from web import form

render = None
urls = None
app = None
myform = None

class index: 
    def GET(self): 
		global	render, myform
		form = myform()
		# make sure you create a copy of the form by calling it (line above)
		# Otherwise changes will appear globally
		return render.formtest(form)

	def POST(self): 
		global render, myform
		form = myform() 
		if not form.validates(): 
			return render.formtest(form)
		else:
			# form.d.boe and form['boe'].value are equivalent ways of
			# extracting the validated arguments from the form.
			return "human: %s, zzd: %s" % (form.d.human, form.d.zzd)

def webinit():
	global render, urls, app, myform
	render = web.template.render('templates/')
	urls = ('/', 'index')
	app = web.application(urls, globals())
	myform = form.Form(form.Textbox("human"), form.Textbox("zzd"))

class index: 
	def GET(self): 
		global myform
		form = myform()
		# make sure you create a copy of the form by calling it (line above)

def createserver():
	global app
	try:
		web.internalerror = web.debugerror
		app.run()
	except:
		print('create web server error.')
		return False
	
if __name__=="__main__":
	webinit()
	createserver()
