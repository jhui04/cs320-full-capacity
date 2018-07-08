import { Component, OnInit, Output, EventEmitter, Injectable } from '@angular/core';
import { Tenant } from '../tenant';
import { HttpClient } from '@angular/common/http';
import { ConfigService } from './config.service'

@Component({
  selector: 'app-user-header',
  templateUrl: './user-header.component.html',
  styleUrls: ['./user-header.component.css'],
  providers: [ConfigService]
})
export class UserHeaderComponent implements OnInit {
	
	tenant: any = [];
	
	@Output() tenantEvent = new EventEmitter<Tenant>();
  
  
  constructor(private http: HttpClient, private configService: ConfigService) { 
    this.configService.getConfig()
      .subscribe(data => {
        this.tenant = data[0];
        this.tenantEvent.emit(this.tenant)
    });
  }

  ngOnInit() {
	  
  }
  
  showConfig() {
    this.configService.getConfig()
      .subscribe(data => this.tenant = data[0]);
	  console.log(this.tenant);
}
  
}
