package com.overwhale.colibri_so.domain.endpoint;

import com.overwhale.colibri_so.domain.entity.UserDetail;
import com.overwhale.colibri_so.domain.service.UserDetailService;
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
