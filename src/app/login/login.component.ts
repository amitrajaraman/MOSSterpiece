import { Component, OnInit } from '@angular/core';
import { SharedService } from 'src/app/shared.service'
import { FormControl, FormGroup, Validators } from '@angular/forms'

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  constructor(private service:SharedService) { }
    form_username = new FormControl('');
    form_password = new FormControl('');

  ngOnInit(): void {
  }
  login():void{
      var data = {
        username: this.form_username.value,
        password: this.form_password.value
      }
      this.service.login(data).subscribe(
        (res)=>{
        console.log(res);
        window.alert(res.toString());
      },
      (error) => {
        console.log("This is backend problem")
        }
      );
      
  }

}

