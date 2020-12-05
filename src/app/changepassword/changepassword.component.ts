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
  form_oldpassword = new FormControl('');
  form_password = new FormControl('');
  form_confirmpw = new FormControl('');

  constructor(private service:SharedService, private router: Router, private messengerService: MessengerService) { }

  ngOnInit(): void {
  }
  update():void{

    if(this.form_password.value != this.form_confirmpw.value){
      window.alert('Error: Passwords do not match.');
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
  }
}
