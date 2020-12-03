import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AboutUsComponent } from './about-us/about-us.component';
import { FileUploadComponent } from './file-upload/file-upload.component';
import { LandingComponent } from './landing/landing.component';
import { LoginComponent } from './login/login.component';
import { SignupComponent } from './signup/signup.component';
import { ProfileComponent } from './profile/profile.component';
import { ChangepasswordComponent } from './changepassword/changepassword.component';
import { WaitingComponent } from './waiting/waiting.component';
import { ViewCurrComponent } from './view-curr/view-curr.component';

const routes: Routes = [
  {path : '', component : LandingComponent },
  {path : 'login', component: LoginComponent },
  {path : 'aboutus', component: AboutUsComponent },
  {path : 'signup', component: SignupComponent},
  {path: 'upload', component: FileUploadComponent},
  {path: 'profile', component: ProfileComponent},
  {path: 'changepassword', component: ChangepasswordComponent},
  {path: 'upload/waiting', component: WaitingComponent},
  {path: 'upload/view', component: ViewCurrComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }