import { Component } from '@angular/core';
import { ServerListingComponent } from './server-listing/server-listing.component';
import { ConfigService } from './server-listing/config.service'

@Component({
 selector: 'app-root',
 templateUrl: './app.component.html',
 styleUrls: ['./app.component.css'],
 providers: [ServerListingComponent, ConfigService]
})
export class AppComponent {

 constructor(private serverListingService: ServerListingComponent) { 
 }

 title = 'Storage Device Analytics';

 selectedTab = 'servers';
 
 message: string;
 
 tenant: string;

 onSelectTab(tab: string): void {
 	this.selectedTab = tab;
 }
 
 receiveMessage($event) {
   this.message = $event
 }

 receiveTenant($event) {
	 this.tenant = $event
 }
 
 public showConfig(){
     this.serverListingService.showConfig();
 }
}