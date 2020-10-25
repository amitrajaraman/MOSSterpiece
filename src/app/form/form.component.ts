import { Component, OnInit } from '@angular/core';
import { Contact } from '../contact';
import { GetpostService } from '../getpost.service';
import { FormControl, FormGroup, Validators } from '@angular/forms'

@Component({
  selector: 'app-form',
  templateUrl: './form.component.html',
  styleUrls: ['./form.component.scss']
})

export class FormComponent implements OnInit {

  data: Contact;
  new_form_name = new FormControl('');
  new_form_email = new FormControl('');
  new_form_comments = new FormControl('');
  selected;
  b_sel=false;

  feedback_form = new FormGroup({
    feed: new FormControl('', Validators.required)
  });

  get f(){
    return this.feedback_form.controls;
  }

  constructor(private GpService: GetpostService) { }

  getdata(): void {
    this.GpService.getData()
      .subscribe(tempVar => {
        this.data = tempVar;
        this.new_form_name.setValue(tempVar.name);
        this.new_form_email.setValue(tempVar.email);
        this.new_form_comments.setValue(tempVar.comment);
        this.feedback_form.patchValue({feed: tempVar.feedback});
      });
  }

  ngOnInit(): void {
    this.getdata();
  }

  submit(): void{
    if( this.f.feed.errors!=null ) {window.alert('Error: Selecting feedback is compulsory');}
    else{
      this.GpService.postData(this.data)
        .subscribe(
          (val) => {
            console.log("Value submitted is", this.data);
            console.log("POST call successful value returned in body", 
                        val);
          },
          response => {
              console.log("POST call in error", response);
              window.alert('There was an error in submitting the form, try again.');
          },
          () => {
              console.log("The POST observable is now completed.");
              window.alert('Form submitted successfully!');
              this.data.email=this.new_form_email.value;
              this.data.name =this.new_form_name.value;
              this.data.comment=this.new_form_comments.value;
              this.data.feedback=this.feedback_form.value.feed;
          }
        );
    }
  }

  onItemChange(value){
   this.selected=value;
   this.b_sel=true;
  }

}
