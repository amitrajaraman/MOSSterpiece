import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms'
import { SharedService } from 'src/app/shared.service'

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.scss']
})

export class SignupComponent implements OnInit {

  form_firstname = new FormControl('');
  form_lastname = new FormControl('');
  form_username = new FormControl('');
  form_email = new FormControl('');
  form_password = new FormControl('');
  form_confirmpw = new FormControl('');

  constructor(private service:SharedService) { }

  ngOnInit(): void {
    
  }

  register():void{

    if(this.form_password.value != this.form_confirmpw.value){
      window.alert('Error: Passwords do not match.');
      return;
    }
    else{
      var data = {
        first_name: this.form_firstname.value,
        last_name: this.form_lastname.value,
        username: this.form_username.value,
        email: this.form_email.value,
        password: this.form_password.value
      }

      this.service.addUser(data).subscribe(res=>{
        console.log(res);
        window.alert("Registration Successfull!");
        this.form_firstname.reset();
        this.form_lastname.reset();
        this.form_username.reset();
        this.form_email.reset();
        this.form_password.reset();
        this.form_confirmpw.reset();
      });
      
    }
  }

}
