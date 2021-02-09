package com.overwhale.colibri_so.domain.service;

import com.overwhale.colibri_so.domain.entity.Intent;
import com.overwhale.colibri_so.domain.repository.IntentRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.vaadin.artur.helpers.CrudService;

import java.time.OffsetDateTime;
import java.util.UUID;

@Service
public class IntentService extends CrudService<Intent, UUID> {
  private final IntentRepository repository;

  public IntentService(@Autowired IntentRepository repository) {
    this.repository = repository;
  }

  @Override
  public Intent update(Intent entity) {
    if (entity.getId() == null) {
      entity.setCreationTime(OffsetDateTime.now());
      entity.setId(UUID.randomUUID());
    } else {
      entity.setLastChangedTime(OffsetDateTime.now());
    }
    return super.update(entity);
  }

  @Override
  protected IntentRepository getRepository() {
    return repository;
  }
}
