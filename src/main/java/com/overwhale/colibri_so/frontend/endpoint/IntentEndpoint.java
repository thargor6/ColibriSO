package com.overwhale.colibri_so.frontend.endpoint;

import com.overwhale.colibri_so.frontend.dto.IntentDto;
import com.overwhale.colibri_so.frontend.service.IntentService;
import com.vaadin.flow.server.connect.Endpoint;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.UUID;

@Endpoint
public class IntentEndpoint extends CrudEndpoint<IntentDto, UUID> {
  private final IntentService service;

  public IntentEndpoint(@Autowired IntentService service) {
    this.service = service;
  }

  @Override
  protected IntentService getService() {
    return service;
  }
}
