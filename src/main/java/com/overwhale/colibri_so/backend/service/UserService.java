package com.overwhale.colibri_so.backend.service;

import com.overwhale.colibri_so.backend.entity.User;
import com.overwhale.colibri_so.backend.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.vaadin.artur.helpers.CrudService;

import java.time.OffsetDateTime;
import java.util.UUID;

@Service
public class UserService extends CrudService<User, UUID> {
  private final UserRepository repository;

  public UserService(@Autowired UserRepository repository) {
    this.repository = repository;
  }

  @Override
  public User update(User entity) {
    if (entity.getId() == null) {
      entity.setCreationTime(OffsetDateTime.now());
      entity.setId(UUID.randomUUID());
    }
    entity.setLastChangedTime(OffsetDateTime.now());
    return super.update(entity);
  }

  public User getByUsername(String username) {
    return getRepository().getByUsername(username);
  }

  @Override
  protected UserRepository getRepository() {
    return repository;
  }
}
