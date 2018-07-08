import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ServerListingComponent } from './server-listing.component';

describe('ServerListingComponent', () => {
  let component: ServerListingComponent;
  let fixture: ComponentFixture<ServerListingComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ServerListingComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ServerListingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
