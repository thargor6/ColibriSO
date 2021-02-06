package com.overwhale.colibri_so.domain.endpoint;

import com.overwhale.colibri_so.domain.entity.Intent;
import com.overwhale.colibri_so.domain.service.IntentService;
import com.vaadin.flow.server.connect.Endpoint;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.UUID;

@Endpoint
public class IntentEndpoint extends CrudEndpoint<Intent, UUID> {
  private final IntentService service;

  public IntentEndpoint(@Autowired IntentService service) {
    this.service = service;
  }

  @Override
  protected IntentService getService() {
    return service;
  }
}
