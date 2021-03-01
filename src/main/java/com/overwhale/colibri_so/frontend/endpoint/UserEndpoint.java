package com.overwhale.colibri_so.frontend.endpoint;

import com.overwhale.colibri_so.backend.entity.User;
import com.overwhale.colibri_so.backend.service.UserService;
import com.vaadin.flow.server.connect.Endpoint;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.UUID;

@Endpoint
public class UserEndpoint extends CrudEndpoint<User, UUID> {
  private final UserService service;

  public UserEndpoint(@Autowired UserService service) {
    this.service = service;
  }

  public User getByUsername(String username) {
    return service.getByUsername(username);
  }

  @Override
  protected UserService getService() {
    return service;
  }
}