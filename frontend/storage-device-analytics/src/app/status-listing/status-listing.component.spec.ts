import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { StatusListingComponent } from './status-listing.component';

describe('StatusListingComponent', () => {
  let component: StatusListingComponent;
  let fixture: ComponentFixture<StatusListingComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ StatusListingComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(StatusListingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
