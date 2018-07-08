import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/do';

@Injectable()
export class ConfigService {
  
  configUrl = '/api/status/';
  defaultStatusUrl = '/api/default_status/';
  
  constructor(private http: HttpClient) { }
  
  

  getConfig(): Observable<any> {
    return this.http.get(this.configUrl);
  }

  getDefaultStatus(): Observable<any> {
  	return this.http.get(this.defaultStatusUrl);
  }
}
