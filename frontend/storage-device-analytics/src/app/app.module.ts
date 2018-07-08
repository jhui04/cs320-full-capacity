import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule, HttpClientXsrfModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';


import { AppComponent } from './app.component';
import { ServerListingComponent } from './server-listing/server-listing.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { NoSanitizePipe } from './dashboard/noSanitize';
import { StatusListingComponent } from './status-listing/status-listing.component';
import { UserHeaderComponent } from './user-header/user-header.component';
import { AlertListingComponent } from './alert-listing/alert-listing.component';

@NgModule({
  declarations: [
    AppComponent,
    ServerListingComponent,
    DashboardComponent,
    StatusListingComponent,
    UserHeaderComponent,
    AlertListingComponent,
    NoSanitizePipe
  ],
  imports: [
    BrowserModule,
  	HttpClientModule,
    HttpClientXsrfModule.withOptions({
      cookieName: 'csrftoken',
      headerName: 'X-CsrfToken'
    }),
  	FormsModule,
    ReactiveFormsModule
  ],
  providers: [
    //{ provide: HTTP_INTERCEPTORS, useClass: HttpClientXsrfModule, multi: true}
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
