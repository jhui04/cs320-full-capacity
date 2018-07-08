import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { Status } from '../status';
import { ServerListing } from '../server-listing';
import { Tenant } from '../tenant';
//import { STATUSES } from '../mock-statuses';
import { HttpClient } from '@angular/common/http';
import { ConfigService } from './config.service'
import { NgForm } from '@angular/forms';
declare var $: any;

@Component({
  selector: 'app-status-listing',
  templateUrl: './status-listing.component.html',
  styleUrls: ['./status-listing.component.css'],
  providers: [ConfigService]
})
export class StatusListingComponent implements OnInit {
  
  @Input() server: ServerListing;
  
  @Input() tenant: Tenant;

  statuses: any = [];
  defaults: any = [];
  
  newStat: Status = new Status();
  
  constructor(private http: HttpClient, private configService: ConfigService) {
    this.configService.getConfig().subscribe(data => this.statuses = data.results);
    this.configService.getDefaultStatus().subscribe(data => {
      this.defaults = data.results;

      this.createDefaultStatuses("addStatusModal");
    });
  }

  modifyValue(field, value) {
    var createEvent = function(name) {
      var event = document.createEvent('Event');
      event.initEvent(name, true, true);
      return event;
    };
    console.log(field, value);

    $(field)[0].dispatchEvent(createEvent('focus'));
    if (value != null) {
      $(field).val(value);
    }
    $(field)[0].dispatchEvent(createEvent('change'));
    $(field)[0].dispatchEvent(createEvent('input'));
    $(field)[0].dispatchEvent(createEvent('blur'));
    console.log("done", field, value);
  }

  createDefaultStatuses(modalName) {
    this.defaults.map(obj => $("#"+modalName+" #default-statuses").append(
      $("<option>" + obj['name'] + "</option>")
      .attr("data-obj", JSON.stringify(obj))));
    var t = this;
    $("#"+modalName+" #metric").change(function() {
      if ($("#"+modalName+" #metric").val() == "SPECIFY_CUSTOM") {
        var m2 = prompt("Enter the custom metric, separated by commas:");
        console.log("option with "+m2+" not found, creating");
          $("#"+modalName+" #metric").append(
            $("<option>" + m2 + "</option>").attr("value", m2)
          );
          t.modifyValue("#"+modalName+" #metric", m2);
      }
    });
    $("#"+modalName+" #operator").change(function() {
      if ($("#"+modalName+" #operator").val() == "exists" || $("#"+modalName+" #operator").val() == "nexist") {
        console.log("exist/nexist");
          t.modifyValue("#"+modalName+" #value", $("#"+modalName+" #operator").val());
      }
    });
    $("#"+modalName+" #default-statuses").change(function() {
      console.log("select change handler");
      var el = $(this).find(":selected");
      console.log("selected=", el);
      if (el.val().length < 1) {
        t.modifyValue("#"+modalName+" #operator", "");
        t.modifyValue("#"+modalName+" #value", "");
        t.modifyValue("#"+modalName+" #metric", "");
      } else {
        var obj = JSON.parse(el.attr("data-obj"));
        console.log("obj = ",obj);
        t.modifyValue("#"+modalName+" #operator", obj['criteria']['operation']);
        t.modifyValue("#"+modalName+" #value", obj['criteria']['value']);
        var m = obj['criteria']['metric'].join(',');
        var found = false;
        $("#"+modalName+" #metric option").each(function() {
          if ($(this).val() == m) {
            console.log("option with "+m+" found:", $(this));
            $("#"+modalName+" #metric option").attr("selected", false);
            $(this).attr("selected", true);
            t.modifyValue("#"+modalName+" #metric", null);
            found = true;
          } else console.log("option val=", $(this).val());
        });
        if (!found) {
          console.log("option with "+m+" not found, creating");
          $("#"+modalName+" #metric").append(
            $("<option>" + m + "</option>").attr("value", m)
          );
          t.modifyValue("#"+modalName+" #metric", m);
        }
      }
    })
  }

  arraysEqual(arr1, arr2){
    if(arr1.length !== arr2.length){
      return false;
    }
    for(var i = arr1.length; i--;){
      if(arr1[i] !== arr2[i]){
        return false;
      }
    }
    return true;
  }

  ngOnInit() {

  }
  
  addStatus(form: NgForm) {
  	this.newStat.newStatus.criteria.metric = form.value.metric;
  	this.newStat.newStatus.criteria.operation = form.value.operator;
  	this.newStat.newStatus.criteria.value = form.value.value;
  	console.log('status-listing tenant', this.tenant);
  	this.newStat.newStatus.user_id = this.tenant.user_id;
  	this.newStat.newStatus.device_id = this.server.id;
    this.newStat.newStatus.criteria.metric = new String(this.newStat.newStatus.criteria.metric).split(",");
    console.log('Trying POST for status');
    console.log(this.newStat.newStatus);
    var t = this;
    var modalName = 'addStatusModal';
  	this.http.post('/api/status/', this.newStat.newStatus)
  	  .subscribe(
  	    res => {
  			 console.log('res', res);
         console.log('statuses before:', this.statuses.length, this.statuses);
         this.statuses.push(res);
         if (res['current_check']) {
          $("li#server-list-" + res['device_id'] + "").removeClass("notTriggered").addClass("triggered");
         }
         console.log('statuses after:', this.statuses.length, this.statuses);
         //$("#addStatusModal").modal("hide");
         $("#addStatusModal button[data-dismiss='modal']").click();
         t.modifyValue("#"+modalName+" #operator", "");
         t.modifyValue("#"+modalName+" #value", "");
         t.modifyValue("#"+modalName+" #metric", "");
         t.modifyValue("#"+modalName+" #default-statuses", "");
  		});
  }
  
  editStatus(form: NgForm) {
	  this.newStat.newStatus.criteria.metric = form.value.metric;
    this.newStat.newStatus.criteria.operation = form.value.operator;
    this.newStat.newStatus.criteria.value = form.value.value;
    console.log('status-listing tenant', this.tenant);
    this.newStat.newStatus.user_id = this.tenant.user_id;
    this.newStat.newStatus.device_id = this.server.id;
    this.newStat.newStatus.id = form.value.id;
    this.newStat.newStatus.active = form.value.enabled;
    this.newStat.newStatus.criteria.metric = new String(this.newStat.newStatus.criteria.metric).split(",");
    console.log('Trying POST for status');
    console.log(this.newStat.newStatus);
    this.http.put('/api/status/' + form.value.id + "/", this.newStat.newStatus)
      .subscribe(
        res => {
         console.log('res', res);
         console.log('statuses before:', this.statuses.length, this.statuses);
         var statuses_for_device = 0;
         for (var i=0; i<this.statuses.length; i++) {
          if (this.statuses[i]['device_id'] == this.server.id) statuses_for_device++;
          if (this.statuses[i]['id'] == res['id']) {
            console.log('found id', this.statuses[i])
            this.statuses[i] = res;
          }
         }
         if (res['current_check']) {
          $("li#server-list-" + res['device_id'] + "").removeClass("notTriggered").addClass("triggered");
         } else if (statuses_for_device == 1) {
          $("li#server-list-" + res['device_id'] + "").removeClass("triggered").addClass("notTriggered");
         }
         console.log('statuses after:', this.statuses.length, this.statuses);
         //$("#addStatusModal").modal("hide");
         $("#editStatusModal button[data-dismiss='modal']").click();
      });
  }
 
  deleteStatus(form: NgForm) {
	  var server_id = this.server.id;
	  this.http.delete('api/status/' + form.value.id + '/')
	  .subscribe(
        res => {
         console.log('statuses before:', this.statuses.length, this.statuses);
         var statuses_for_device = 0;
         for (var i=0; i<this.statuses.length; i++) {
          if (this.statuses[i]['device_id'] == this.server.id) statuses_for_device++;
          if (this.statuses[i]['id'] == form.value.id) {
            console.log('found id', this.statuses[i])
            this.statuses[i] = {};
          }
         }
		 if (statuses_for_device == 1) {
          $("li#server-list-" + server_id + "").removeClass("triggered").addClass("notTriggered");
         }
         console.log('statuses after:', this.statuses.length, this.statuses);
         //$("#addStatusModal").modal("hide");
         $("#editStatusModal button[data-dismiss='modal']").click();
      });
  }
	  
  openEdit(status, edit) {
    console.log('edit', status, edit);
    var m = status['criteria']['metric'];
    if ($("#editStatusModal #metric option[value='" + m + "']").length == 0) {
      $("#editStatusModal #metric").append($("<option>"+m+"</option>").attr("value", m));
      console.log('added option with', m);
    }
    edit.form.patchValue({
      'metric': status['criteria']['metric'],
      'operator': status['criteria']['operation'],
      'value': status['criteria']['value'],
      'enabled': status['active'],
      'id': status['id']
    });
  }

  filteredStatuses(server_id) {
      return this.statuses
        .filter(status => status.device_id == server_id)
        .sort(status => !status.current_check);
  }

  showConfig() {
    this.configService.getConfig().subscribe(data => this.statuses = data.results);
    console.log(this.statuses.results)
  }
}
