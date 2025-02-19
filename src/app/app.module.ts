import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { PreHeaderComponent } from './pre-header/pre-header.component';
import { LandingComponent } from './landing/landing.component';
import { LoginComponent } from './login/login.component';
import { AboutUsComponent } from './about-us/about-us.component';
import { SignupComponent } from './signup/signup.component';
import { FileUploadComponent } from './file-upload/file-upload.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatIconModule } from '@angular/material/icon';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { FileService, SharedService } from './shared.service';
import {FormsModule,ReactiveFormsModule} from '@angular/forms';
import { ProfileComponent } from './profile/profile.component';
import { ChangepasswordComponent } from './changepassword/changepassword.component';
import { ViewCurrComponent } from './view-curr/view-curr.component';
import { WaitingComponent } from './waiting/waiting.component';

@NgModule({
  declarations: [
    AppComponent,
    PreHeaderComponent,
    LandingComponent,
    LoginComponent,
    AboutUsComponent,
    SignupComponent,
    FileUploadComponent,
    ProfileComponent,
    ChangepasswordComponent,
    ViewCurrComponent,
    WaitingComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    BrowserAnimationsModule,
    MatToolbarModule,
    MatIconModule,
    MatButtonModule,
    MatCardModule,
    MatProgressBarModule,
    FormsModule,
    ReactiveFormsModule
  ],
  providers: [SharedService, FileService],
  bootstrap: [AppComponent]
})
export class AppModule { }
