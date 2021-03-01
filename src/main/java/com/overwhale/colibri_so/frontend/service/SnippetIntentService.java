package com.overwhale.colibri_so.frontend.service;

import com.overwhale.colibri_so.backend.entity.SnippetIntent;
import com.overwhale.colibri_so.backend.repository.SnippetIntentRepository;
import com.overwhale.colibri_so.frontend.dto.SnippetIntentDto;
import com.overwhale.colibri_so.frontend.mapper.SnippetIntentMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Service;
import org.vaadin.artur.helpers.CrudService;

import java.util.Optional;
import java.util.UUID;

@Service
public class SnippetIntentService extends CrudService<SnippetIntentDto, UUID> {
  private final SnippetIntentRepository repository;

  public SnippetIntentService(@Autowired SnippetIntentRepository repository) {
    this.repository = repository;
  }

  public SnippetIntentDto update(SnippetIntentDto dto) {
    SnippetIntent entity = SnippetIntentMapper.INSTANCE.dtoToEntiy(dto);
    return SnippetIntentMapper.INSTANCE.entityToDto(repository.save(entity));
  }

  @Override
  protected JpaRepository<SnippetIntentDto, UUID> getRepository() {
    return null;
  }

  public Optional<SnippetIntentDto> get(UUID id) {
    return repository.findById(id).map(e -> SnippetIntentMapper.INSTANCE.entityToDto(e));
  }

  public void delete(UUID id) {
    repository.deleteById(id);
  }

  public Page<SnippetIntentDto> list(Pageable pageable) {
    return repository.findAll(pageable).map(e -> SnippetIntentMapper.INSTANCE.entityToDto(e));
  }

  public int count() {
    return (int) repository.count();
  }
}
