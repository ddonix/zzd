import web
from web import form

render = web.template.render('templates/')

urls = ('/', 'index')
app = web.application(urls, globals())

myform = form.Form( 
	form.Textbox("human"), 
	form.Textbox("zzd"))

class index: 
	def GET(self): 
		form = myform()
		# make sure you create a copy of the form by calling it (line above)
		# Otherwise changes will appear globally
		return render.formtest(form)

	def POST(self): 
		form = myform() 
		if not form.validates(): 
			return render.formtest(form)
		else:
			# form.d.boe and form['boe'].value are equivalent ways of
			# extracting the validated arguments from the form.
			return "! human: %s, zzd: %s" % (form.d.human, form.d.zzd)

def createwebserver():
	web.internalerror = web.debugerror
	app.run()
	print('web server error.')
	return False

if __name__=="__main__":
	gg = globals()
	ggg = dict(gg)
	for g in ggg:
		print(g,ggg[g])
#	createwebserver()
