import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AboutUsComponent } from './about-us/about-us.component';
import { FileUploadComponent } from './file-upload/file-upload.component';
import { LandingComponent } from './landing/landing.component';
import { LoginComponent } from './login/login.component';
import { SignupComponent } from './signup/signup.component';

const routes: Routes = [
  {path : '', component : LandingComponent },
  {path : 'login', component: LoginComponent },
  {path : 'aboutus', component: AboutUsComponent },
  {path : 'signup', component: SignupComponent},
  {path: 'upload', component: FileUploadComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }


/*const routes: Routes = [
  { path: 'feedback', component: ContactFormComponent },
  { path: 'contact', component: ContactPageComponent },
  { path: '**', redirectTo: 'contact', pathMatch: 'prefix' },
]; */