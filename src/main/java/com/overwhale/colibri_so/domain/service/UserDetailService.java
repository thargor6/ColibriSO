package com.overwhale.colibri_so.domain.service;

import com.overwhale.colibri_so.domain.entity.UserDetail;
import com.overwhale.colibri_so.domain.repository.UserDetailRepository;
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
