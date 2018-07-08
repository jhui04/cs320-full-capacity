import { Component, OnInit, AfterViewInit, Input } from '@angular/core';
import { ServerListing } from '../server-listing';
declare var $: any;
@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit, AfterViewInit {

  @Input() server: ServerListing;

  constructor() { }

  buildServerInfoTree(o, item, i){
		item += "<ul id='info-tree-"+parseInt(i)+"' class='info-tree'>";
		var item_mod = false;
		for (var key in o) {
			if (o[key] == null) {
				item += "<li>" + key + ": null</li>";
			} else if (typeof(o[key]) === "object") {
			  item += "<li onclick=\"$('#info-tree-"+new String(100*i)+"').toggle()\" class='info-tree-link'>" + new String(key) + "</li>";
			  item = this.buildServerInfoTree(o[key], item, 100*i);
			} else {
			  item += "<li>" + key + ": " + o[key] + "</li>";
			}
			i++;
			item_mod = true;
		}
		if (!item_mod) item += "<li>(empty)</li>";
		item += "</ul>";
		return item
	}

  ngOnInit() {
  }

  ngAfterViewInit() {

  }

  
}
