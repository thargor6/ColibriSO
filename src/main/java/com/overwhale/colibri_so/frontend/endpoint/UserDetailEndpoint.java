package com.overwhale.colibri_so.frontend.endpoint;

import com.overwhale.colibri_so.backend.entity.UserDetail;
import com.overwhale.colibri_so.backend.service.UserDetailService;
import com.vaadin.flow.server.connect.Endpoint;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.UUID;

@Endpoint
public class UserDetailEndpoint extends CrudEndpoint<UserDetail, UUID> {
  private final UserDetailService service;

  public UserDetailEndpoint(@Autowired UserDetailService service) {
    this.service = service;
  }

  @Override
  protected UserDetailService getService() {
    return service;
  }
}
