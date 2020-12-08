import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms'
import { MessengerService, SharedService } from 'src/app/shared.service'

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.scss']
})

export class SignupComponent implements OnInit {
  /**Form field for first name */
  form_firstname = new FormControl('');
  /**Form field for last name */
  form_lastname = new FormControl('');
  /**Form field for username */
  form_username = new FormControl('');
  /**Form field for email */
  form_email = new FormControl('');
  /**Form field for password */
  form_password = new FormControl('');
  /**Form field to confirm password */
  form_confirmpw = new FormControl('');

  constructor(private service:SharedService, public messengerService:MessengerService) { }

  ngOnInit(): void {
    
  }
  /**method to register user if the conditions are satisfied, i.e. passwords match, email/username is not taken */
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

      this.service.addUser(data).subscribe(
        (res)=>{
          if(res["safe"])
          {
            console.log(res);
            window.alert("Registration Successful!");
          }
          else
          {
            window.alert(res["message"]);
          }
        this.form_firstname.reset();
        this.form_lastname.reset();
        this.form_username.reset();
        this.form_email.reset();
        this.form_password.reset();
        this.form_confirmpw.reset();
      }

      );
      
    }
  }

}
