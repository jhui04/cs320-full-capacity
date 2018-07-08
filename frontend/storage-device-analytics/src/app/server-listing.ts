import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable()

export class ServerListing {
    id: string;
	name: string;
	serialNumberInserv: string;
	nodes: any;
	updated: string;
	date: string;
	system: any;
	capacity: any;
	performance: any;
	disks: any
	authorized: any;
	
	constructor() { }
	
}