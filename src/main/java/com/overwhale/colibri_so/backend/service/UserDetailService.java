package com.overwhale.colibri_so.backend.service;

import com.overwhale.colibri_so.backend.entity.UserDetail;
import com.overwhale.colibri_so.backend.repository.UserDetailRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.vaadin.artur.helpers.CrudService;

import java.util.UUID;

@Service
public class UserDetailService extends CrudService<UserDetail, UUID> {
  private final UserDetailRepository repository;

  public UserDetailService(@Autowired UserDetailRepository repository) {
    this.repository = repository;
  }

  @Override
  protected UserDetailRepository getRepository() {
    return repository;
  }
}
