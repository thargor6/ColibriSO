package com.overwhale.colibri_so.domain.service;


import com.overwhale.colibri_so.domain.entity.SnippetIntent;
import com.overwhale.colibri_so.domain.entity.SnippetTag;
import com.overwhale.colibri_so.domain.repository.SnippetIntentRepository;
import com.overwhale.colibri_so.domain.repository.SnippetTagRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.vaadin.artur.helpers.CrudService;

import java.util.UUID;

@Service
public class SnippetIntentService extends CrudService<SnippetIntent, UUID> {
  private final SnippetIntentRepository repository;

  public SnippetIntentService(@Autowired SnippetIntentRepository repository) {
    this.repository = repository;
  }

  @Override
  protected SnippetIntentRepository getRepository() {
    return repository;
  }
}
