import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { Status } from '../status';
import { ServerListing } from '../server-listing';
//import { STATUSES } from '../mock-statuses';
import { HttpClient } from '@angular/common/http';
import { ConfigService } from './config.service'

@Component({
  selector: 'app-alert-listing',
  templateUrl: './alert-listing.component.html',
  styleUrls: ['./alert-listing.component.css'],
  providers: [ConfigService]
})
export class AlertListingComponent implements OnInit {
  
  @Input() server: ServerListing;

  statuses: any = [];
  
  constructor(private http: HttpClient, private configService: ConfigService) {
    this.configService.getConfig().subscribe(data => this.statuses = data.results);
  }

  filteredStatuses() {
    return this.statuses.filter(status => status.current_check == true && status.active == true);
  }

  ngOnInit() {
  }
  
  addStatus() {
	
  }
  
  editStatus() {
	  
  }

  openView(status) {
    console.log('click', status);
    
  }

  showConfig() {
  this.configService.getConfig().subscribe(data => this.statuses = data.results);
  console.log(this.statuses.results)
  }
}
