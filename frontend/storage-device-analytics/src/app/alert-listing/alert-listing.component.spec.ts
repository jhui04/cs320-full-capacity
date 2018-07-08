import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AlertListingComponent } from './alert-listing.component';

describe('AlertListingComponent', () => {
  let component: AlertListingComponent;
  let fixture: ComponentFixture<AlertListingComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AlertListingComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AlertListingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
