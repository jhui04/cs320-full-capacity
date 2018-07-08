import { Component, OnInit, Output, EventEmitter, Injectable } from '@angular/core';
import { ServerListing } from '../server-listing';
import { HttpClient } from '@angular/common/http';
import { ConfigService } from './config.service'

@Component({
  selector: 'app-server-listing',
  templateUrl: './server-listing.component.html',
  styleUrls: ['./server-listing.component.css'],
  providers: [ConfigService]
})
export class ServerListingComponent implements OnInit {
	
	servers: any = [];
	
	selectedServer: ServerListing;
	
	@Output() messageEvent = new EventEmitter<ServerListing>();
  
  
  constructor(private http: HttpClient, private configService: ConfigService) { 
  this.configService.getConfig()
    .subscribe(data => this.servers = data);
  }

  ngOnInit() {
  }
  
  onSelect(serverListing: ServerListing): void {
    this.selectedServer = serverListing;
	this.messageEvent.emit(this.selectedServer)
  }
  
  showConfig() {
  this.configService.getConfig()
    .subscribe(data => this.servers = data);
	console.log(this.servers);
  }
  
}
