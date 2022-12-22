from flask import Flask,request,render_template,url_for,flash,redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,EmailField,IntegerField
from wtforms.validators import DataRequired,email_validator
from git import Repo
import os

app1 = Flask(__name__)
app1.config['SECRET_KEY'] = 'MY secret key' # to use forms we need secret key
path = "C:/Users/DataGrokr/Desktop/DG_intern_Assignmenst/python_assignments/notepad+extraction/notepad-tracker-main/notes"
git_path = "C:/Users/DataGrokr/Desktop/DG_intern_Assignmenst/python_assignments/notepad+extraction/notepad-tracker-main/"
@app1.route('/')
def homepage():

    notes = list(os.walk(path))[0][2]
    if not notes:
        return render_template('homepage.html',data = 'Empty')
    else:
        data = {}
        for note in notes:
            n = open(f"{path}/{note}",'r')
            data.update({note.replace('.txt',''):n.read()}) 
            n.close()
        return render_template('homepage.html',data = data)

class Addnote(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    Desc = StringField('Description',validators=[DataRequired()])
    add = SubmitField('Add Note')    

@app1.route('/addnote',methods=["GET","POST"])
def addnote():
    form = Addnote()
    #title_to_add = None
    #Desc_to_add = None
    notes = list(os.walk(path))[0][2]
    if notes:
        t = []
        for n in notes:
            t.append(n.replace('.txt',''))
        notes = t
    else:
        pass
    if request.method == "POST":
        title_to_add = request.form['title']
        Desc_to_add = request.form['Desc']
        try:
            note = open(path+'/'+title_to_add + '.txt','x')
            note.write(Desc_to_add)
            note.close()
            form.title.data = ''
            form.Desc.data = ''
            notes.append(title_to_add)
            repo = Repo(git_path)
            repo.git.add('.')
            repo.git.commit('-m', f'added note {title_to_add}')

            flash(F"Note {title_to_add} added Successfully")
            return render_template('addnote.html',form = form,notes = notes)
        except FileExistsError:
            flash(F"Note {title_to_add} Already exist try different Title")
            return render_template('addnote.html',form = form,notes = notes)
    else:
        return render_template('addnote.html',form = form,notes = notes)

class editform(FlaskForm):
    Desc = StringField('Description',validators=[DataRequired()])
    edit = SubmitField('Edit Note')

@app1.route('/editnote/<title>',methods=['GET','POST'])
def editnote(title):
    note = open(path+'/'+title+'.txt','r')
    msg = note.read()
    note.close()
    form = editform()
    if request.method =='POST':
        note = open(path+'/'+title+'.txt','w')
        Desc_to_edit = request.form['Desc']
        note.write(Desc_to_edit)
        note.close()
        repo = Repo(git_path)
        repo.git.add('.')
        repo.git.commit('-m', f'edited the note {title}')

        flash(F"Note {title} Edited Successfully")
        return redirect('/')
    else:
        return render_template('edit.html',form = form, msg = msg,title = title)

class deleteform(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    delete = SubmitField('Delete Note')

@app1.route('/deletenote',methods=['GET','POST'])
def deletenote():
    form = deleteform()
    notes = list(os.walk(path))[0][2]
    if notes:
        t = []
        for n in notes:
            t.append(n.replace('.txt',''))
        notes = t
    else:
        pass
    #note_to_delete = 
    if request.method == 'POST':
        note_to_delete = request.form['title']
        try:
            os.remove(path+'/'+note_to_delete+'.txt')
            repo = Repo(git_path)
            repo.git.add('.')
            repo.git.commit('-m', f'Deleted the note {note_to_delete}')
            notes.pop(note_to_delete)
            flash(f"The note {note_to_delete} was Deleted Successfully")
            form.title.data = ''
            return render_template('deletenote.html',form=form, notes = notes)
        except:
            flash(f"The note {note_to_delete} does not exits ")
            return render_template('deletenote.html',form = form,notes = notes)
    else:
        return render_template('deletenote.html',form = form,notes = notes)

if __name__ == '__main__':
    app1.run(debug=True)