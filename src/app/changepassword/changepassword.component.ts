import { Component, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { Router } from '@angular/router';
import { MessengerService, SharedService } from '../shared.service';

@Component({
  selector: 'app-changepassword',
  templateUrl: './changepassword.component.html',
  styleUrls: ['./changepassword.component.scss']
})
export class ChangepasswordComponent implements OnInit {
  /**
   * Form fields for old password
   */
  form_oldpassword = new FormControl('');
  /**Form field for new password */
  form_password = new FormControl('');
  /**Form field for confirming new password */
  form_confirmpw = new FormControl('');
  /**
   * Basically checks if the new password is equal to the 'confirm new password field' and also checks if the old password is correct
   * @param service 
   * @param router 
   * @param messengerService 
   */
  constructor(private service:SharedService, private router: Router, public messengerService: MessengerService) { }

  ngOnInit(): void {  }
  /** 
   * sends request to the backend to change the password if the criteria of the fields are met.
   */
  update():void{

    if(this.form_password.value != this.form_confirmpw.value){
      window.alert('Error: Passwords do not match.');
      return;
    }
    else if(this.form_password.value == "" || this.form_confirmpw.value == ""){
      window.alert('Enter a new password.');
      return;
    }
    else{
      var data = {
        oldpassword: this.form_oldpassword.value,
        newpassword: this.form_password.value
      }

      this.service.changepw(data).subscribe(res=>{
        console.log(res);
        window.alert(res.message);
        this.form_oldpassword.reset();
        this.form_password.reset();
        this.form_confirmpw.reset();
      });
      
    }

    this.router.navigate(['/profile']);
  }
}